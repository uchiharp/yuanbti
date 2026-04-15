#!/usr/bin/env python3
"""Production import script with batch processing."""

import json
import psycopg2
import time
from pathlib import Path
import sys

DATA_DIR = Path(__file__).parent

# Read DB URL from file
with open("/tmp/db9_final_url.txt", "r") as f:
    DB_URL = f.read().strip()

print(f"DB URL loaded ({len(DB_URL)} chars)")

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
    print("Connecting to database...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    # Clear existing data
    print("Clearing existing data...")
    cur.execute("DELETE FROM dialogues")
    cur.execute("DELETE FROM character_profiles")
    cur.execute("DELETE FROM story_pages")
    conn.commit()
    print("  Tables cleared.")
    
    # Get all JSON files (exclude metadata/progress)
    print("Scanning for JSON files...")
    all_files = sorted(DATA_DIR.rglob("*.json"))
    files = [f for f in all_files if f.name not in ["metadata.json", "progress.json"]]
    total_files = len(files)
    print(f"Found {total_files} story files")
    
    # Batch processing parameters
    FILES_PER_BATCH = 200
    MAX_DIALOGUES_PER_BATCH = 10000  # Avoid too large batch
    
    # Statistics
    total_stories = 0
    total_dialogues = 0
    char_story_counts = {}
    char_dialogue_counts = {}
    errors = []
    
    start_time = time.time()
    
    # Process in batches of files
    for batch_start in range(0, total_files, FILES_PER_BATCH):
        batch_end = min(batch_start + FILES_PER_BATCH, total_files)
        batch_files = files[batch_start:batch_end]
        batch_num = batch_start // FILES_PER_BATCH + 1
        total_batches = (total_files + FILES_PER_BATCH - 1) // FILES_PER_BATCH
        
        print(f"\n{'='*60}")
        print(f"Batch {batch_num}/{total_batches}: files {batch_start+1}-{batch_end} of {total_files}")
        
        # Collect data from this batch of files
        batch_stories = []
        batch_dialogues = []
        batch_char_story = {}
        batch_char_dialogue = {}
        batch_errors = []
        
        file_start = time.time()
        for fpath in batch_files:
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
                batch_stories.append((
                    title, category, subcat, characters,
                    json.dumps(content, ensure_ascii=False) if content else None,
                    raw_wikitext or None, source_url or None, crawled_at or None,
                    str(rel_path)
                ))
                
                # Update character story counts
                for ch in characters:
                    batch_char_story[ch] = batch_char_story.get(ch, 0) + 1
                
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
                        batch_char_dialogue[speaker] = batch_char_dialogue.get(speaker, 0) + 1
                    
                    batch_dialogues.append((
                        title, category, speaker or '(旁白)', text,
                        dtype, emotion or None, line_idx
                    ))
                    
            except Exception as e:
                batch_errors.append((str(fpath), str(e)))
                continue
        
        file_time = time.time() - file_start
        print(f"  Parsed {len(batch_files)} files in {file_time:.1f}s ({file_time/len(batch_files):.2f}s/file)")
        
        # Insert stories (batch)
        if batch_stories:
            insert_start = time.time()
            cur.executemany(
                """INSERT INTO story_pages 
                (title, category, sub_category, characters, content_json, 
                 raw_wikitext, source_url, crawled_at, json_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                batch_stories
            )
            total_stories += len(batch_stories)
            insert_time = time.time() - insert_start
            print(f"  Inserted {len(batch_stories)} stories in {insert_time:.1f}s")
        
        # Insert dialogues (in chunks to avoid huge batch)
        if batch_dialogues:
            dialogue_chunks = [batch_dialogues[i:i+MAX_DIALOGUES_PER_BATCH] 
                              for i in range(0, len(batch_dialogues), MAX_DIALOGUES_PER_BATCH)]
            for chunk_num, chunk in enumerate(dialogue_chunks):
                insert_start = time.time()
                cur.executemany(
                    """INSERT INTO dialogues 
                    (story_title, category, speaker, text, dialogue_type, emotion, line_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    chunk
                )
                insert_time = time.time() - insert_start
                total_dialogues += len(chunk)
                if len(dialogue_chunks) > 1:
                    print(f"    Dialogue chunk {chunk_num+1}/{len(dialogue_chunks)}: {len(chunk)} rows in {insert_time:.1f}s")
                else:
                    print(f"  Inserted {len(chunk)} dialogues in {insert_time:.1f}s")
        
        # Commit this batch
        conn.commit()
        
        # Update global character counts
        for ch, count in batch_char_story.items():
            char_story_counts[ch] = char_story_counts.get(ch, 0) + count
        for ch, count in batch_char_dialogue.items():
            char_dialogue_counts[ch] = char_dialogue_counts.get(ch, 0) + count
        
        # Update errors
        errors.extend(batch_errors)
        
        # Progress stats
        elapsed = time.time() - start_time
        files_processed = min(batch_end, total_files)
        rate = files_processed / elapsed if elapsed > 0 else 0
        eta = (total_files - files_processed) / rate if rate > 0 else 0
        
        print(f"  Batch stats: {total_stories} stories, {total_dialogues} dialogues")
        print(f"  Overall: {files_processed}/{total_files} files ({files_processed*100/total_files:.1f}%)")
        print(f"  Rate: {rate:.1f} files/s, ETA: {eta/60:.1f} min")
    
    # Update character_profiles table
    print(f"\n{'='*60}")
    print("Updating character_profiles table...")
    all_chars = set(char_story_counts.keys()) | set(char_dialogue_counts.keys())
    char_updates = []
    for name in all_chars:
        sc = char_story_counts.get(name, 0)
        dc = char_dialogue_counts.get(name, 0)
        char_updates.append((name, sc, dc))
    
    if char_updates:
        update_start = time.time()
        # Process in chunks of 1000
        chunk_size = 1000
        for i in range(0, len(char_updates), chunk_size):
            chunk = char_updates[i:i+chunk_size]
            cur.executemany(
                """INSERT INTO character_profiles (name, story_count, dialogue_count)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (name) DO UPDATE SET
                     story_count = character_profiles.story_count + EXCLUDED.story_count,
                     dialogue_count = character_profiles.dialogue_count + EXCLUDED.dialogue_count""",
                chunk
            )
        conn.commit()
        update_time = time.time() - update_start
        print(f"  Updated {len(char_updates)} character profiles in {update_time:.1f}s")
    
    # Get final counts
    cur.execute("SELECT COUNT(*) FROM story_pages")
    final_stories = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dialogues")
    final_dialogues = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM character_profiles")
    final_chars = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    total_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print("=== IMPORT COMPLETE ===")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"Files processed: {total_files - len(errors)}/{total_files}")
    print(f"Errors: {len(errors)}")
    if errors and len(errors) <= 10:
        print("Sample errors:")
        for fp, err in errors[:10]:
            print(f"  {fp}: {err}")
    
    print(f"\nFinal database counts:")
    print(f"  story_pages: {final_stories}")
    print(f"  dialogues: {final_dialogues}")
    print(f"  character_profiles: {final_chars}")
    
    # Show top categories
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
