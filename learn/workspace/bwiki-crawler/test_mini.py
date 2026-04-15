#!/usr/bin/env python3
import json
import psycopg2
import subprocess
from pathlib import Path
import time

DATA_DIR = Path(__file__).parent

def get_db_url():
    result = subprocess.run(
        ['/Users/sunwenyong/.local/bin/db9', 'db', 'connect', 'learn_test'],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.splitlines():
        if line.strip().startswith('postgresql://'):
            return line.strip()
    raise RuntimeError('Cannot get DB URL')

def main():
    print("1. Getting DB URL...")
    db_url = get_db_url()
    print("2. Connecting...")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Clear test data
    cur.execute("DELETE FROM dialogues WHERE story_title LIKE 'MINI-%'")
    cur.execute("DELETE FROM story_pages WHERE title LIKE 'MINI-%'")
    conn.commit()
    
    # Get 5 files
    all_files = sorted(DATA_DIR.rglob("*.json"))
    files = [f for f in all_files if f.name not in ["metadata.json", "progress.json"]][:5]
    
    print(f"3. Processing {len(files)} files...")
    
    for fpath in files:
        rel = fpath.relative_to(DATA_DIR)
        print(f"  - {rel}")
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        title = "MINI-" + data.get('title', fpath.stem)
        chars = data.get('characters', [])
        content = data.get('content', [])
        
        # Determine category
        parts = rel.parts
        category = parts[0] if parts else "unknown"
        subcat = "/".join(parts[:2]) if len(parts) >= 2 else category
        
        # Insert story
        cur.execute(
            """INSERT INTO story_pages (title, category, sub_category, characters, content_json, json_file)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
            (title, category, subcat, chars, json.dumps(content, ensure_ascii=False) if content else None, str(rel))
        )
        story_id = cur.fetchone()[0]
        
        # Insert first 3 dialogues
        for idx, item in enumerate(content[:3]):
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
        
        print(f"    -> id {story_id}, {len(chars)} chars, {len(content)} content items")
    
    conn.commit()
    
    # Count
    cur.execute("SELECT COUNT(*) FROM story_pages WHERE title LIKE 'MINI-%'")
    stories = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dialogues WHERE story_title LIKE 'MINI-%'")
    dialogues = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    print(f"\n4. Result: {stories} stories, {dialogues} dialogues inserted")
    print("Test passed!")

if __name__ == "__main__":
    main()
