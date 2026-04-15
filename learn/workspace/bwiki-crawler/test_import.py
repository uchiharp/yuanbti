#!/usr/bin/env python3
import json
import psycopg2
import sys
import subprocess
from pathlib import Path

DB9_CLI = "/Users/sunwenyong/.local/bin/db9"
DB_NAME = "learn_test"

def get_db_url():
    """Get db9 connection string from CLI arg or db9 CLI."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    result = subprocess.run(
        [DB9_CLI, "db", "connect", DB_NAME],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.splitlines():
        if line.strip().startswith("postgresql://"):
            return line.strip()
    raise RuntimeError(f"Cannot get db URL: {result.stdout}\n{result.stderr}")

def main():
    db_url = get_db_url()
    print(f"Connecting to: {db_url[:60]}...")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Test query
    cur.execute("SELECT COUNT(*) FROM story_pages")
    count = cur.fetchone()[0]
    print(f"Current story_pages count: {count}")
    
    # Test inserting one file
    data_dir = Path(__file__).parent
    test_file = data_dir / "男主/约会/左慈-约会_月亮酒杯.json"
    print(f"Testing with file: {test_file}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    title = data.get('title', test_file.stem)
    characters = data.get('characters', [])
    content = data.get('content', [])
    
    print(f"Title: {title}")
    print(f"Characters: {characters}")
    print(f"Content items: {len(content)}")
    
    # Insert one record
    cur.execute(
        """INSERT INTO story_pages (title, category, sub_category, characters, content_json)
           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (title, '约会', '男主/约会', characters, json.dumps(content, ensure_ascii=False))
    )
    inserted_id = cur.fetchone()[0]
    conn.commit()
    print(f"Inserted story_pages id: {inserted_id}")
    
    # Insert dialogues
    for idx, item in enumerate(content[:5]):
        dtype = item.get('type', 'raw')
        speaker = item.get('speaker', '')
        text = item.get('text', '')
        emotion = item.get('emotion', '')
        cur.execute(
            """INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (title, '约会', speaker or '(旁白)', text, dtype, emotion or None, idx)
        )
    conn.commit()
    print(f"Inserted {min(5, len(content))} dialogue rows")
    
    cur.close()
    conn.close()
    print("Test successful!")

if __name__ == "__main__":
    main()
