#!/usr/bin/env python3
"""极小批量：每次只读 10 个 story"""
import psycopg2, json

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"
READ_BATCH = 10
INSERT_SIZE = 200

conn = psycopg2.connect(DB_URL, connect_timeout=60)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SET db9.dml_table_scan_max_rows = 0")

# 检查当前状态
cur.execute("SELECT COUNT(*) FROM dialogues")
existing = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
existing_stories = cur.fetchone()[0]
print(f"Current: {existing} dialogues, {existing_stories} stories", flush=True)

# 获取所有 story titles
print("Loading story titles...", flush=True)
cur.execute("SELECT title FROM story_pages WHERE content_json IS NOT NULL ORDER BY title")
all_titles = [r[0] for r in cur.fetchall()]
print(f"Total: {len(all_titles)} stories", flush=True)

# 找出还需要处理的
if existing_stories > 0:
    cur.execute("SELECT DISTINCT story_title FROM dialogues")
    done_titles = set(r[0] for r in cur.fetchall())
    todo_titles = [t for t in all_titles if t not in done_titles]
    print(f"Already done: {len(done_titles)}, Remaining: {len(todo_titles)}", flush=True)
else:
    todo_titles = all_titles
    # 清空
    print("Clearing...", flush=True)
    cur.execute("DELETE FROM dialogues")

total_inserted = 0
for i in range(0, len(todo_titles), READ_BATCH):
    batch_titles = todo_titles[i:i+READ_BATCH]
    
    # 逐个读取（避免大查询超时）
    rows = []
    for title in batch_titles:
        try:
            cur.execute("SELECT title, category, content_json FROM story_pages WHERE title = %s AND content_json IS NOT NULL", (title,))
            r = cur.fetchone()
            if r:
                rows.append(r)
        except Exception as e:
            print(f"  Error reading {title}: {e}", flush=True)
    
    if not rows:
        continue
    
    # Python 端拆分
    batch = []
    for title, category, content_json in rows:
        content = json.loads(content_json) if isinstance(content_json, str) else content_json
        for idx, item in enumerate(content):
            if not isinstance(item, dict) or not item.get('type'):
                continue
            batch.append((
                title, category,
                item.get('speaker') or '(旁白)',
                item.get('text', ''),
                item.get('type', 'raw'),
                item.get('emotion', ''),
                idx
            ))
    
    if not batch:
        continue
    
    # 写入
    conn.autocommit = False
    try:
        for j in range(0, len(batch), INSERT_SIZE):
            chunk = batch[j:j+INSERT_SIZE]
            cur.executemany(
                "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                chunk
            )
            conn.commit()
        total_inserted += len(batch)
        if (i + READ_BATCH) % 100 == 0 or i + READ_BATCH >= len(todo_titles):
            print(f"  {min(i+READ_BATCH, len(todo_titles))}/{len(todo_titles)} stories, {total_inserted} dialogues", flush=True)
    except Exception as e:
        print(f"  Error inserting batch at {i}: {e}", flush=True)
        conn.rollback()
    conn.autocommit = True

# 最终统计
cur.execute("SELECT COUNT(*) FROM dialogues")
d = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
s = cur.fetchone()[0]
print(f"\nDone! {d} dialogues from {s} stories", flush=True)

conn.close()
