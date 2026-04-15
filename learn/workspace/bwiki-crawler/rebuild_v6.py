#!/usr/bin/env python3
"""Python 端拆分 + 批量写入，绕过 SQL 超时限制"""
import psycopg2, json, sys
from collections import defaultdict

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"
BATCH_STORIES = 100  # 每次读 100 个 story
INSERT_SIZE = 500    # 每次写入 500 条

conn = psycopg2.connect(DB_URL, connect_timeout=30)
conn.autocommit = True
cur = conn.cursor()

# 调大 DML 限制
cur.execute("SET db9.dml_table_scan_max_rows = 0")

# 清空
print("Clearing dialogues...", flush=True)
cur.execute("DELETE FROM dialogues")
print("  Done", flush=True)

# 获取总数
cur.execute("SELECT COUNT(*) FROM story_pages WHERE content_json IS NOT NULL")
total_stories = cur.fetchone()[0]
print(f"Total stories: {total_stories}", flush=True)

offset = 0
total_inserted = 0
total_stories_done = 0

while offset < total_stories:
    # 读取一批 story
    cur.execute("""
        SELECT title, category, content_json 
        FROM story_pages WHERE content_json IS NOT NULL 
        ORDER BY title LIMIT %s OFFSET %s
    """, (BATCH_STORIES, offset))
    stories = cur.fetchall()
    
    if not stories:
        break
    
    # Python 端拆分
    batch = []
    for title, category, content_json in stories:
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
    
    # 批量写入
    conn.autocommit = False
    for i in range(0, len(batch), INSERT_SIZE):
        chunk = batch[i:i+INSERT_SIZE]
        cur.executemany(
            "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            chunk
        )
        conn.commit()
    conn.autocommit = True
    
    total_inserted += len(batch)
    total_stories_done += len(stories)
    offset += BATCH_STORIES
    print(f"  Progress: {total_stories_done}/{total_stories} stories, {total_inserted} dialogues", flush=True)

# 最终统计
cur.execute("SELECT COUNT(*) FROM dialogues")
d = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
s = cur.fetchone()[0]
print(f"\nDone! {d} dialogues from {s} stories", flush=True)

conn.close()
