#!/usr/bin/env python3
"""Chunked import script - processes files in batches with commits."""

import json
import psycopg2
import sys
import time
from pathlib import Path
import subprocess

DATA_DIR = Path(__file__).parent

def get_db_url():
    """Get fresh DB URL."""
    result = subprocess.run(
        ["/Users/sunwenyong/.local/bin/db9", "db", "connect", "learn_test"],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.splitlines():
        if line.strip().startswith("postgresql://"):
            return line.strip()
    raise RuntimeError("Cannot get DB URL")

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

def process_batch(files_batch, conn, stats, errors):
    """Process a batch of files and commit."""
    cur = conn.cursor()
    
    story_batch = []
    dialogue_batch = []
    char_story_counts = {}
    char_dialogue_counts = {}
    
    for fpath in files_batch:
        try:
            rel_path = fpath.relative_to(DATA_DIR)
            category, subcat = get_category_subcategory(rel_path)
            
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            title = data.get('title', fpath.stem)
            characters = data.get('characters', [])
            content = data.get('content', [])
            source_url = data.get('source_url', '')
            crawled_at = data.get('crawled_at', '')
            raw_wikitext = data.get('raw_wikitext', '')
            
            # Story row
            story_batch.append((
                title, category, subcat, characters,
                json.dumps(content, ensure_ascii=False) if content else None,
                raw_wikitext or None, source_url or None, crawled_at or None,
                str(rel_path)
            ))
            
            # Character counts
            for ch in characters:
                char_story_counts[ch] = char_story_counts.get(ch, 0) + 1
            
            # Dialogue rows
            for line_idx, item in enumerate(content):
                if not isinstance(item, dict):
                    continue
                dtype = item.get('type', 'raw')
                speaker = item.get('speaker', '')
                text = item.get('text', '')
                emotion = item.get('emotion', '')
                
                if speaker and dtype == 'dialogue':
                    char_dialogue_counts[speaker] = char_dialogue_counts.get(speaker, 0) + 1
                
                dialogue_batch.append((
                    title, category, speaker or '(旁白)', text,
                    dtype, emotion or None, line_idx
                ))
                
        except Exception as e:
            errors.append((str(fpath), str(e)))
            continue
    
    # Insert stories
    if story_batch:
        cur.executemany(
            """INSERT INTO story_pages 
            (title, category, sub_category, characters, content_json, 
             raw_wikitext, source_url, crawled_at, json_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            story_batch
        )
        stats['stories'] += len(story_batch)
    
    # Insert dialogues
    if dialogue_batch:
        cur.executemany(
            """INSERT INTO dialogues 
            (story_title, category, speaker, text, dialogue_type, emotion, line_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            dialogue_batch
        )
        stats['dialogues'] += len(dialogue_batch)
    
    conn.commit()
    cur.close()
    
    # Update character counts in stats
    for ch, count in char_story_counts.items():
        stats['char_story_counts'][ch] = stats['char_story_counts'].get(ch, 0) + count
    for ch, count in char_dialogue_counts.items():
        stats['char_dialogue_counts'][ch] = stats['char_dialogue_counts'].get(ch, 0) + count
    
    return len(files_batch) - len(errors)

def main():
    print("Getting DB URL...")
    db_url = get_db_url()
    print(f"Connecting to DB...")
    conn = psycopg2.connect(db_url)
    conn.autocommit = False
    
    # Clear tables
    print("Clearing existing data...")
    cur = conn.cursor()
    cur.execute("DELETE FROM dialogues")
    cur.execute("DELETE FROM character_profiles")
    cur.execute("DELETE FROM story_pages")
    conn.commit()
    cur.close()
    print("  Tables cleared.")
    
    # Get files
    print("Scanning files...")
    all_files = sorted(DATA_DIR.rglob("*.json"))
    files = [f for f in all_files if f.name not in ["metadata.json", "progress.json"]]
    total_files = len(files)
    print(f"Found {total_files} story files")
    
    # Stats
    stats = {
        'stories': 0,
        'dialogues': 0,
        'char_story_counts': {},
        'char_dialogue_counts': {}
    }
    errors = []
    
    # Process in chunks
    CHUNK_SIZE = 100
    chunks = [files[i:i+CHUNK_SIZE] for i in range(0, total_files, CHUNK_SIZE)]
    
    start_time = time.time()
    
    for i, chunk in enumerate(chunks):
        chunk_start = time.time()
        processed = process_batch(chunk, conn, stats, errors)
        
        elapsed = time.time() - start_time
        chunk_elapsed = time.time() - chunk_start
        rate = (i+1) * CHUNK_SIZE / elapsed if elapsed > 0 else 0
        remaining = (len(chunks) - (i+1)) * (chunk_elapsed) if chunk_elapsed > 0 else 0
        
        print(f"Chunk {i+1}/{len(chunks)}: {processed}/{len(chunk)} files | "
              f"Stories: {stats['stories']} | Dialogues: {stats['dialogues']} | "
              f"Rate: {rate:.1f} files/s | ETA: {remaining:.0f}s")
    
    # Update character_profiles
    print("\nUpdating character_profiles...")
    all_chars = set(stats['char_story_counts'].keys()) | set(stats['char_dialogue_counts'].keys())
    char_updates = []
    for name in all_chars:
        sc = stats['char_story_counts'].get(name, 0)
        dc = stats['char_dialogue_counts'].get(name, 0)
        char_updates.append((name, sc, dc))
    
    if char_updates:
        cur = conn.cursor()
        cur.executemany(
            """INSERT INTO character_profiles (name, story_count, dialogue_count)
               VALUES (%s, %s, %s)
               ON CONFLICT (name) DO UPDATE SET
                 story_count = character_profiles.story_count + EXCLUDED.story_count,
                 dialogue_count = character_profiles.dialogue_count + EXCLUDED.dialogue_count""",
            char_updates
        )
        conn.commit()
        cur.close()
    
    # Final counts
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM story_pages")
    final_stories = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dialogues")
    final_dialogues = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM character_profiles")
    final_chars = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    total_time = time.time() - start_time
    
    print(f"\n=== IMPORT COMPLETE ===")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}min)")
    print(f"Files processed: {total_files - len(errors)}/{total_files}")
    print(f"Errors: {len(errors)}")
    
    if errors and len(errors) <= 5:
        for fp, err in errors[:5]:
            print(f"  {fp}: {err}")
    
    print(f"\nDatabase counts:")
    print(f"  story_pages: {final_stories}")
    print(f"  dialogues: {final_dialogues}")
    print(f"  character_profiles: {final_chars}")
    
    # Quick category breakdown
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT category, COUNT(*) FROM story_pages GROUP BY category ORDER BY count DESC LIMIT 10")
    print(f"\nTop categories:")
    for cat, cnt in cur.fetchall():
        print(f"  {cat}: {cnt}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
