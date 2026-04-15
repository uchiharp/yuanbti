#!/usr/bin/env python3
"""分批补导缺失的 dialogues，避免内存/超时问题"""
import json, psycopg2, sys
from collections import defaultdict

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"
BATCH_STORIES = 300  # 每批处理 300 个 story

def main():
    offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    conn = psycopg2.connect(DB_URL, connect_timeout=30)
    conn.autocommit = False
    cur = conn.cursor()
    
    # 获取已有 dialogues
    print("Loading existing dialogues...", flush=True)
    cur.execute("SELECT story_title, line_order FROM dialogues")
    existing = defaultdict(set)
    for title, order in cur.fetchall():
        existing[title].add(order)
    print(f"  Existing: {len(existing)} stories", flush=True)
    
    # 获取 story_pages（分批）
    cur.execute("SELECT title, category, content_json FROM story_pages WHERE content_json IS NOT NULL ORDER BY title OFFSET %s LIMIT %s", (offset, BATCH_STORIES))
    stories = cur.fetchall()
    print(f"  Batch {offset}-{offset+len(stories)}: {len(stories)} stories", flush=True)
    
    batch = []
    missing_stories = 0
    total_missing = 0
    
    for title, category, content_json in stories:
        content = json.loads(content_json) if isinstance(content_json, str) else content_json
        existing_orders = existing.get(title, set())
        story_missing = 0
        
        for idx, item in enumerate(content):
            if not isinstance(item, dict) or idx in existing_orders:
                continue
            dtype = item.get('type', 'raw')
            speaker = item.get('speaker', '(旁白)') or '(旁白)'
            text = item.get('text', '')
            emotion = item.get('emotion', '')
            batch.append((title, category, speaker, text, dtype, emotion, idx))
            story_missing += 1
        
        if story_missing > 0:
            missing_stories += 1
            total_missing += story_missing
    
    print(f"  Missing: {missing_stories} stories, {total_missing} dialogues", flush=True)
    
    if not batch:
        print("  Nothing to insert", flush=True)
        conn.close()
        return
    
    # 插入
    INSERT_SIZE = 1000
    for i in range(0, len(batch), INSERT_SIZE):
        chunk = batch[i:i+INSERT_SIZE]
        cur.executemany(
            "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            chunk
        )
        conn.commit()
        print(f"  Inserted {min(i+INSERT_SIZE, len(batch))}/{len(batch)}", flush=True)
    
    conn.close()
    print(f"  Batch done! Total inserted: {len(batch)}", flush=True)

if __name__ == "__main__":
    main()
