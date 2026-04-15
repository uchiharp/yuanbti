#!/usr/bin/env python3
import json
import psycopg2
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent

with open("/tmp/db9_final_url.txt", "r") as f:
    DB_URL = f.read().strip()

print("Connecting...")
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Clear test data
cur.execute("DELETE FROM dialogues WHERE story_title LIKE 'TEST10-%'")
cur.execute("DELETE FROM story_pages WHERE title LIKE 'TEST10-%'")
conn.commit()

# Get 10 files
all_files = sorted(DATA_DIR.rglob("*.json"))
files = [f for f in all_files if f.name not in ["metadata.json", "progress.json"]][:10]

print(f"Processing {len(files)} files...")
start = time.time()

for i, fpath in enumerate(files):
    print(f"[{i+1}/{len(files)}] {fpath.relative_to(DATA_DIR)}")
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    title = "TEST10-" + data.get('title', fpath.stem)
    chars = data.get('characters', [])
    content = data.get('content', [])
    
    # Simple category
    parts = fpath.relative_to(DATA_DIR).parts
    category = parts[0] if parts else "unknown"
    subcat = "/".join(parts[:2]) if len(parts) >= 2 else category
    
    # Insert story
    cur.execute(
        """INSERT INTO story_pages (title, category, sub_category, characters, content_json, json_file)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (title, category, subcat, chars, json.dumps(content, ensure_ascii=False) if content else None, str(fpath.relative_to(DATA_DIR)))
    )
    story_id = cur.fetchone()[0]
    
    # Insert first 5 dialogues
    inserted = 0
    for idx, item in enumerate(content[:5]):
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
        inserted += 1
    
    print(f"  -> id {story_id}, chars {len(chars)}, content {len(content)}, inserted {inserted}")

conn.commit()

cur.execute("SELECT COUNT(*) FROM story_pages WHERE title LIKE 'TEST10-%'")
stories = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM dialogues WHERE story_title LIKE 'TEST10-%'")
dialogues = cur.fetchone()[0]

cur.close()
conn.close()

print(f"\nDone in {time.time()-start:.2f}s")
print(f"Inserted: {stories} stories, {dialogues} dialogues")
