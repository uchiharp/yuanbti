#!/usr/bin/env python3
import json
import psycopg2
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent
DB_URL = open("/tmp/db_url_new.txt").read().strip()

# Get 10 JSON files, excluding metadata.json and progress.json
all_files = sorted(DATA_DIR.rglob("*.json"))
files = []
for f in all_files:
    if f.name in ["metadata.json", "progress.json"]:
        continue
    files.append(f)
    if len(files) >= 10:
        break

print(f"Processing {len(files)} files")

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Clear test data
cur.execute("DELETE FROM dialogues WHERE story_title LIKE 'TEST%'")
cur.execute("DELETE FROM story_pages WHERE title LIKE 'TEST%'")
conn.commit()

for fpath in files:
    rel_path = fpath.relative_to(DATA_DIR)
    print(f"  {rel_path}")
    
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    title = "TEST-" + data.get('title', fpath.stem)
    chars = data.get('characters', [])
    content = data.get('content', [])
    
    # Determine category from path
    parts = rel_path.parts
    category = parts[0] if parts else "unknown"
    subcat = "/".join(parts[:2]) if len(parts) >= 2 else category
    
    # Insert story
    cur.execute(
        """INSERT INTO story_pages (title, category, sub_category, characters, content_json, json_file)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (title, category, subcat, chars, json.dumps(content, ensure_ascii=False) if content else None, str(rel_path))
    )
    story_id = cur.fetchone()[0]
    
    # Insert dialogues
    for idx, item in enumerate(content[:3]):  # just first 3
        if not isinstance(item, dict):
            continue
        dtype = item.get('type', 'raw')
        speaker = item.get('speaker', '')
        text = item.get('text', '')
        emotion = item.get('emotion', '')
        cur.execute(
            """INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (title, category, speaker or '(旁白)', text, dtype, emotion or None, idx)
        )
    
    print(f"    -> story {story_id}, {len(content)} content items")

conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM story_pages WHERE title LIKE 'TEST%'")
story_cnt = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM dialogues WHERE story_title LIKE 'TEST%'")
dialogue_cnt = cur.fetchone()[0]
print(f"\nInserted: {story_cnt} stories, {dialogue_cnt} dialogues")

cur.close()
conn.close()
print("Test successful!")
