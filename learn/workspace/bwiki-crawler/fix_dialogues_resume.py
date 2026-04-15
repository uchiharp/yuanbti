#!/usr/bin/env python3
"""补导缺失的 dialogues — 断点续传版
每次跑 200 个故事，写入进度文件，可反复执行直到补完。
"""
import json, psycopg2, time, sys, os
from pathlib import Path

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"
BATCH_STORIES = 200  # 每批处理多少个故事
PROGRESS_FILE = Path(__file__).parent / ".fix_progress.json"

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"done_titles": [], "total_inserted": 0, "total_skipped": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False)

def main():
    progress = load_progress()
    done_set = set(progress["done_titles"])
    
    conn = psycopg2.connect(DB_URL, connect_timeout=60)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SET db9.dml_table_scan_max_rows = 0")

    # 获取所有 story 的对话数
    cur.execute("SELECT title, jsonb_array_length(content_json) as cnt FROM story_pages WHERE content_json IS NOT NULL")
    story_counts = {row[0]: row[1] for row in cur.fetchall()}

    # 获取 dialogues 表中每个 story 的对话数
    cur.execute("SELECT story_title, COUNT(*) as cnt FROM dialogues GROUP BY story_title")
    dialogue_counts = {row[0]: row[1] for row in cur.fetchall()}

    # 找出还缺的（排除已完成的）
    todo = []
    total_missing = 0
    for title, expected in story_counts.items():
        if title in done_set:
            continue
        actual = dialogue_counts.get(title, 0)
        if actual < expected:
            todo.append((title, expected - actual))
            total_missing += expected - actual

    if not todo:
        print("✅ All stories complete!")
        PROGRESS_FILE.exists() and PROGRESS_FILE.unlink()
        conn.close()
        return

    print(f"Remaining: {len(todo)} stories, {total_missing} lines to insert")
    print(f"Already done: {len(done_set)} stories, {progress['total_inserted']} lines inserted")
    print(f"Batch size: {BATCH_STORIES} stories per run")
    
    # 取一批
    batch_titles = set(t for t, _ in todo[:BATCH_STORIES])
    batch_missing = sum(m for _, m in todo[:BATCH_STORIES])

    # 获取这批 story 的数据
    cur.execute("""
        SELECT title, category, content_json 
        FROM story_pages 
        WHERE content_json IS NOT NULL 
        AND title = ANY(%s)
    """, (list(batch_titles),))
    stories = cur.fetchall()

    inserted = 0
    skipped = 0
    batch_rows = []
    start = time.time()

    for title, category, content_json in stories:
        content = json.loads(content_json) if isinstance(content_json, str) else content_json
        # 获取已有行号
        cur.execute("SELECT line_order FROM dialogues WHERE story_title = %s", (title,))
        existing_orders = set(row[0] for row in cur.fetchall())

        for idx, item in enumerate(content):
            if not isinstance(item, dict) or idx in existing_orders:
                skipped += 1
                continue
            dtype = item.get('type', 'raw')
            speaker = item.get('speaker', '(旁白)') or '(旁白)'
            text = item.get('text', '')
            emotion = item.get('emotion', '')
            batch_rows.append((title, category, speaker, text, dtype, emotion, idx))

            if len(batch_rows) >= 200:
                from psycopg2.extras import execute_values
                execute_values(
                    cur,
                    "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES %s",
                    batch_rows,
                    page_size=200
                )
                inserted += len(batch_rows)
                batch_rows.clear()
                elapsed = time.time() - start
                rate = inserted / elapsed if elapsed > 0 else 0
                print(f"  {inserted}/{batch_missing} ({inserted*100//batch_missing}%) {rate:.0f}/s", flush=True)

    if batch_rows:
        from psycopg2.extras import execute_values
        execute_values(
            cur,
            "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES %s",
            batch_rows,
            page_size=len(batch_rows)
        )
        inserted += len(batch_rows)
        batch_rows.clear()

    # 更新进度
    progress["done_titles"].extend(list(batch_titles))
    progress["total_inserted"] += inserted
    progress["total_skipped"] += skipped
    save_progress(progress)

    elapsed = time.time() - start
    print(f"\n✅ Batch done! Inserted: {inserted}, Skipped: {skipped}, Time: {elapsed:.0f}s")
    print(f"Progress: {len(done_set) + len(batch_titles)}/{len(todo) + len(done_set)} stories done")

    # 显示还剩多少
    remaining = len(todo) - len(batch_titles)
    if remaining > 0:
        print(f"Remaining: ~{remaining} stories — run again to continue")
    else:
        print("🎉 All done!")
        PROGRESS_FILE.exists() and PROGRESS_FILE.unlink()

    conn.close()

if __name__ == "__main__":
    main()
