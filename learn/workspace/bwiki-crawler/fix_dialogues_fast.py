#!/usr/bin/env python3
"""快速补导缺失的 dialogues：批量查询去重，避免逐 story 查询"""
import json, psycopg2
from collections import defaultdict

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()

# 1. 一次性获取所有已有 dialogues 的 (story_title, line_order)
print("Loading existing dialogues...")
cur.execute("SELECT story_title, line_order FROM dialogues")
existing = defaultdict(set)
for title, order in cur.fetchall():
    existing[title].add(order)
print(f"  Existing: {len(existing)} stories, {sum(len(v) for v in existing.values())} rows")

# 2. 获取所有 story_pages
print("Loading story_pages...")
cur.execute("SELECT title, category, content_json FROM story_pages WHERE content_json IS NOT NULL")
stories = cur.fetchall()
print(f"  Stories: {len(stories)}")

# 3. 批量构建插入数据
print("Building insert batch...")
batch = []
missing_stories = 0
missing_dialogues = 0

for title, category, content_json in stories:
    content = json.loads(content_json) if isinstance(content_json, str) else content_json
    existing_orders = existing.get(title, set())
    
    has_missing = False
    for idx, item in enumerate(content):
        if not isinstance(item, dict):
            continue
        if idx in existing_orders:
            continue
        has_missing = True
        dtype = item.get('type', 'raw')
        speaker = item.get('speaker', '(旁白)') or '(旁白)'
        text = item.get('text', '')
        emotion = item.get('emotion', '')
        batch.append((title, category, speaker, text, dtype, emotion, idx))
    
    if has_missing:
        missing_stories += 1
        missing_dialogues += len([i for i in range(len(content)) if i not in existing_orders and isinstance(content[i], dict)])

print(f"  Missing: {missing_stories} stories, {len(batch)} dialogues to insert")

if not batch:
    print("All complete!")
    conn.close()
    exit()

# 4. 批量插入
print("Inserting...")
inserted = 0
BATCH_SIZE = 2000
for i in range(0, len(batch), BATCH_SIZE):
    chunk = batch[i:i+BATCH_SIZE]
    cur.executemany(
        "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        chunk
    )
    inserted += len(chunk)
    conn.commit()
    if inserted % 10000 < BATCH_SIZE:
        print(f"  Progress: {inserted}/{len(batch)}")

conn.close()
print(f"\nDone! Inserted: {inserted}")
