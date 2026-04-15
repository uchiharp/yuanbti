#!/usr/bin/env python3
"""Final import script for BWIKI data into db9."""

import json
import psycopg2
import sys
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent
# Get DB URL from command line or file
if len(sys.argv) > 1:
    DB_URL = sys.argv[1]
else:
    # Get fresh URL from db9 CLI
    import subprocess
    result = subprocess.run(
        ["/Users/sunwenyong/.local/bin/db9", "db", "connect", "learn_test"],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.splitlines():
        if line.strip().startswith("postgresql://"):
            DB_URL = line.strip()
            break
    else:
        print("Cannot get DB URL")
        sys.exit(1)

print(f"DB URL: {DB_URL[:60]}...")

# Directory mapping
DIR_MAP = {
    "密探/传唤": ("密探传唤", "密探/传唤"),
    "密探/故事": ("密探故事", "密探/故事"),
    "密探/留音": ("密探留音", "密探/留音"),
    "密探/羁绊": ("密探羁绊", "密探/羁绊"),
    "剧情/主线": ("主线剧情", "剧情/主线"),
    "剧情/活动": ("活动剧情", "剧情/活动"),
    "剧情/恋念": ("恋念剧情", "剧情/恋念"),
    "男主/红鸾花笺": ("红鸾花笺", "男主/红鸾花笺"),
    "男主/恋念之音": ("恋念之音", "男主/恋念之音"),
    "男主/约会": ("约会", "男主/约会"),
    "男主/留音": ("男主留音", "男主/留音"),
    "鸢记": ("鸢记", "鸢记"),
}

def get_category_subcategory(rel_path):
    parts = rel_path.parts
    for key in sorted(DIR_MAP.keys(), key=len, reverse=True):
        key_parts = key.split("/")
        if len(parts) >= len(key_parts) and parts[:len(key_parts)] == tuple(key_parts):
            return DIR_MAP[key]
    return (parts[0] if parts else "unknown", 
            "/".join(parts[:2]) if len(parts) >= 2 else parts[0] if parts else "unknown")

def main():
    # Connect to DB
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    # Clear existing data
    print("Clearing existing data...")
    cur.execute("DELETE FROM dialogues")
    cur.execute("DELETE FROM character_profiles")
    cur.execute("DELETE FROM story_pages")
    conn.commit()
    print("  All tables cleared.")
    
    # Collect JSON files, exclude metadata.json and progress.json
    print("Scanning for JSON files...")
    all_files = sorted(DATA_DIR.rglob("*.json"))
    json_files = []
    for f in all_files:
        if f.name in ["metadata.json", "progress.json"]:
            continue
        json_files.append(f)
    
    total_files = len(json_files)
    print(f"Found {total_files} story JSON files (excluding metadata/progress)")
    
    # Batch buffers
    story_batch = []
    dialogue_batch = []
    char_story_counts = {}
    char_dialogue_counts = {}
    errors = []
    
    # Batch sizes
    STORY_BATCH_SIZE = 200
    DIALOGUE_BATCH_SIZE = 1000
    
    start_time = time.time()
    
    for idx, fpath in enumerate(json_files):
        # Progress reporting
        if idx % 100 == 0:
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 0
            remaining = (total_files - idx) / rate if rate > 0 else 0
            print(f"Progress: {idx}/{total_files} ({idx*100/total_files:.1f}%) | "
                  f"Elapsed: {elapsed:.1f}s | "
                  f"Rate: {rate:.1f} files/s | "
                  f"ETA: {remaining:.0f}s")
        
        try:
            rel_path = fpath.relative_to(DATA_DIR)
            category, subcat = get_category_subcategory(rel_path)
            
            # Read JSON
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            title = data.get('title', fpath.stem)
            characters = data.get('characters', [])
            content = data.get('content', [])
            source_url = data.get('source_url', '')
            crawled_at = data.get('crawled_at', '')
            raw_wikitext = data.get('raw_wikitext', '')
            
            # Prepare story row
            story_batch.append((
                title, category, subcat, characters,
                json.dumps(content, ensure_ascii=False) if content else None,
                raw_wikitext or None, source_url or None, crawled_at or None,
                str(rel_path)
            ))
            
            # Update character story counts
            for ch in characters:
                char_story_counts[ch] = char_story_counts.get(ch, 0) + 1
            
            # Prepare dialogue rows
            for line_idx, item in enumerate(content):
                if not isinstance(item, dict):
                    continue
                dtype = item.get('type', 'raw')
                speaker = item.get('speaker', '')
                text = item.get('text', '')
                emotion = item.get('emotion', '')
                
                # Update character dialogue counts
                if speaker and dtype == 'dialogue':
                    char_dialogue_counts[speaker] = char_dialogue_counts.get(speaker, 0) + 1
                
                dialogue_batch.append((
                    title, category, speaker or '(旁白)', text,
                    dtype, emotion or None, line_idx
                ))
            
            # Flush batches if full
            if len(story_batch) >= STORY_BATCH_SIZE:
                cur.executemany(
                    """INSERT INTO story_pages 
                    (title, category, sub_category, characters, content_json, 
                     raw_wikitext, source_url, crawled_at, json_file)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    story_batch
                )
                story_batch.clear()
                conn.commit()
            
            if len(dialogue_batch) >= DIALOGUE_BATCH_SIZE:
                cur.executemany(
                    """INSERT INTO dialogues 
                    (story_title, category, speaker, text, dialogue_type, emotion, line_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    dialogue_batch
                )
                dialogue_batch.clear()
                conn.commit()
                
        except Exception as e:
            errors.append((str(fpath), str(e)))
            if len(errors) <= 3:
                print(f"  Error: {fpath}: {e}")
            continue
    
    # Flush remaining batches
    if story_batch:
        cur.executemany(
            """INSERT INTO story_pages 
            (title, category, sub_category, characters, content_json, 
             raw_wikitext, source_url, crawled_at, json_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            story_batch
        )
        conn.commit()
    
    if dialogue_batch:
        cur.executemany(
            """INSERT INTO dialogues 
            (story_title, category, speaker, text, dialogue_type, emotion, line_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            dialogue_batch
        )
        conn.commit()
    
    # Update character_profiles
    print("\nUpdating character_profiles...")
    all_chars = set(char_story_counts.keys()) | set(char_dialogue_counts.keys())
    char_updates = []
    for name in all_chars:
        sc = char_story_counts.get(name, 0)
        dc = char_dialogue_counts.get(name, 0)
        char_updates.append((name, sc, dc))
    
    # Batch insert/update
    if char_updates:
        cur.executemany(
            """INSERT INTO character_profiles (name, story_count, dialogue_count)
               VALUES (%s, %s, %s)
               ON CONFLICT (name) DO UPDATE SET
                 story_count = character_profiles.story_count + EXCLUDED.story_count,
                 dialogue_count = character_profiles.dialogue_count + EXCLUDED.dialogue_count""",
            char_updates
        )
        conn.commit()
    
    # Get final counts
    cur.execute("SELECT COUNT(*) FROM story_pages")
    story_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dialogues")
    dialogue_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM character_profiles")
    char_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    total_time = time.time() - start_time
    print(f"\n=== IMPORT COMPLETE ===")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}min)")
    print(f"Files processed: {total_files - len(errors)}/{total_files}")
    print(f"Errors: {len(errors)}")
    if errors and len(errors) <= 10:
        for fp, err in errors[:10]:
            print(f"  {fp}: {err}")
    
    print(f"\nDatabase counts:")
    print(f"  story_pages: {story_count}")
    print(f"  dialogues: {dialogue_count}")
    print(f"  character_profiles: {char_count}")
    
    # Quick category breakdown
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT category, COUNT(*) FROM story_pages GROUP BY category ORDER BY count DESC LIMIT 10")
    print(f"\nTop categories:")
    for cat, cnt in cur.fetchall():
        print(f"  {cat}: {cnt}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
