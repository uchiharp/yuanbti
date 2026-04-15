#!/usr/bin/env python3
"""Direct import using pre-fetched DB URL."""

import json
import psycopg2
import sys
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent

# Read DB URL from file
with open("/tmp/db9_final_url.txt", "r") as f:
    DB_URL = f.read().strip()

print(f"DB URL length: {len(DB_URL)}")
print(f"First 80 chars: {DB_URL[:80]}...")

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
    print("Connecting to DB...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    print("Clearing tables...")
    cur.execute("DELETE FROM dialogues")
    cur.execute("DELETE FROM character_profiles")
    cur.execute("DELETE FROM story_pages")
    conn.commit()
    print("  Tables cleared.")
    
    # Get files
    print("Scanning files...")
    all_files = sorted(DATA_DIR.rglob("*.json"))
    files = [f for f in all_files if f.name not in ["metadata.json", "progress.json"]]
    total = len(files)
    print(f"Found {total} story files")
    
    # Process in batches
    BATCH_SIZE = 200
    errors = []
    char_story = {}
    char_dialogue = {}
    
    start = time.time()
    
    for batch_idx in range(0, total, BATCH_SIZE):
        batch = files[batch_idx:batch_idx+BATCH_SIZE]
        batch_start = time.time()
        
        story_rows = []
        dialogue_rows = []
        
        for fpath in batch:
            try:
                rel = fpath.relative_to(DATA_DIR)
                category, subcat = get_category_subcategory(rel)
                
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                title = data.get('title', fpath.stem)
                chars = data.get('characters', [])
                content = data.get('content', [])
                source_url = data.get('source_url', '')
                crawled_at = data.get('crawled_at', '')
                wikitext = data.get('raw_wikitext', '')
                
                # Story row
                story_rows.append((
                    title, category, subcat, chars,
                    json.dumps(content, ensure_ascii=False) if content else None,
                    wikitext or None, source_url or None, crawled_at or None,
                    str(rel)
                ))
                
                # Character story counts
                for ch in chars:
                    char_story[ch] = char_story.get(ch, 0) + 1
                
                # Dialogue rows
                for idx, item in enumerate(content):
                    if not isinstance(item, dict):
                        continue
                    dtype = item.get('type', 'raw')
                    speaker = item.get('speaker', '')
                    text = item.get('text', '')
                    emotion = item.get('emotion', '')
                    
                    if speaker and dtype == 'dialogue':
                        char_dialogue[speaker] = char_dialogue.get(speaker, 0) + 1
                    
                    dialogue_rows.append((
                        title, category, speaker or '(旁白)', text,
                        dtype, emotion or None, idx
                    ))
                    
            except Exception as e:
                errors.append((str(fpath), str(e)))
                continue
        
        # Insert batch
        if story_rows:
            cur.executemany(
                """INSERT INTO story_pages 
                (title, category, sub_category, characters, content_json, 
                 raw_wikitext, source_url, crawled_at, json_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                story_rows
            )
        
        if dialogue_rows:
            cur.executemany(
                """INSERT INTO dialogues 
                (story_title, category, speaker, text, dialogue_type, emotion, line_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                dialogue_rows
            )
        
        conn.commit()
        
        elapsed = time.time() - start
        batch_elapsed = time.time() - batch_start
        processed = min(batch_idx + BATCH_SIZE, total)
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total - processed) / rate if rate > 0 else 0
        
        print(f"Batch {batch_idx//BATCH_SIZE + 1}/{(total+BATCH_SIZE-1)//BATCH_SIZE}: "
              f"{processed}/{total} files | "
              f"Stories: {batch_idx + len(story_rows)} | "
              f"Dialogues: {sum(len(content) for _,_,_,content,_,_,_,_,_ in story_rows)} | "
              f"Rate: {rate:.1f} files/s | ETA: {eta:.0f}s")
    
    # Update character profiles
    print("\nUpdating character_profiles...")
    all_chars = set(char_story.keys()) | set(char_dialogue.keys())
    for name in all_chars:
        sc = char_story.get(name, 0)
        dc = char_dialogue.get(name, 0)
        cur.execute(
            """INSERT INTO character_profiles (name, story_count, dialogue_count)
               VALUES (%s, %s, %s)
               ON CONFLICT (name) DO UPDATE SET
                 story_count = character_profiles.story_count + EXCLUDED.story_count,
                 dialogue_count = character_profiles.dialogue_count + EXCLUDED.dialogue_count""",
            (name, sc, dc)
        )
    conn.commit()
    
    # Final counts
    cur.execute("SELECT COUNT(*) FROM story_pages")
    story_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dialogues")
    dialogue_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM character_profiles")
    char_cnt = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    total_time = time.time() - start
    
    print(f"\n=== IMPORT COMPLETE ===")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}min)")
    print(f"Files processed: {total - len(errors)}/{total}")
    print(f"Errors: {len(errors)}")
    if errors and len(errors) <= 5:
        for fp, err in errors[:5]:
            print(f"  {fp}: {err}")
    
    print(f"\nDatabase counts:")
    print(f"  story_pages: {story_cnt}")
    print(f"  dialogues: {dialogue_cnt}")
    print(f"  character_profiles: {char_cnt}")
    
    # Category breakdown
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
