#!/usr/bin/env python3
"""补导缺失的 dialogues：对比 story_pages 和 dialogues，补缺"""
import json, psycopg2
from pathlib import Path

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()

# 获取所有 story 的对话总数
cur.execute("SELECT title, jsonb_array_length(content_json) as cnt FROM story_pages WHERE content_json IS NOT NULL")
story_counts = {row[0]: row[1] for row in cur.fetchall()}

# 获取 dialogues 表中每个 story 的对话数
cur.execute("SELECT story_title, COUNT(*) as cnt FROM dialogues GROUP BY story_title")
dialogue_counts = {row[0]: row[1] for row in cur.fetchall()}

# 找出缺失的
missing = {}
total_missing = 0
for title, expected in story_counts.items():
    actual = dialogue_counts.get(title, 0)
    if actual < expected:
        missing[title] = expected - actual
        total_missing += expected - actual

print(f"Stories: {len(story_counts)}, Stories in dialogues: {len(dialogue_counts)}")
print(f"Stories with missing dialogues: {len(missing)}, Total missing: {total_missing}")

if total_missing == 0:
    print("All complete!")
    conn.close()
    exit()

# 从 story_pages 的 content_json 补导
cur.execute("SELECT title, category, content_json FROM story_pages WHERE content_json IS NOT NULL")
stories = cur.fetchall()

batch = []
inserted = 0
skipped = 0

for title, category, content_json in stories:
    if title not in missing:
        continue
    content = json.loads(content_json) if isinstance(content_json, str) else content_json
    # 获取已有对话的行号，避免重复
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
        batch.append((title, category, speaker, text, dtype, emotion, idx))
        
        if len(batch) >= 1000:
            cur.executemany(
                "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                batch
            )
            inserted += len(batch)
            batch.clear()
            conn.commit()
            if inserted % 10000 < 1000:
                print(f"  Inserted: {inserted}/{total_missing}")

if batch:
    cur.executemany(
        "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        batch
    )
    inserted += len(batch)
    conn.commit()

conn.close()
print(f"\nDone! Inserted: {inserted}, Skipped (dup): {skipped}")
