#!/usr/bin/env python3
"""Simple import of BWIKI data into db9."""

import json
import psycopg2
import sys
from pathlib import Path
import time

DATA_DIR = Path(__file__).parent
DB_URL = sys.argv[1] if len(sys.argv) > 1 else open("/tmp/db_url.txt").read().strip()

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
    return (parts[0] if parts else "unknown", "/".join(parts[:2]) if len(parts) >= 2 else parts[0] if parts else "unknown")

def main():
    print(f"Connecting to DB...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    # Clear existing data
    print("Clearing existing data...")
    cur.execute("DELETE FROM dialogues")
    cur.execute("DELETE FROM story_pages")
    cur.execute("DELETE FROM character_profiles")
    conn.commit()
    
    # Get all JSON files
    json_files = sorted(DATA_DIR.rglob("*.json"))
    total = len(json_files)
    print(f"Found {total} JSON files")
    
    story_batch = []
    dialogue_batch = []
    char_story = {}
    char_dialogue = {}
    errors = []
    
    start = time.time()
    
    for i, fpath in enumerate(json_files):
        if i % 100 == 0:
            elapsed = time.time() - start
            print(f"Processed {i}/{total} ({100*i/total:.1f}%), {elapsed:.1f}s")
        
        try:
            rel_path = fpath.relative_to(DATA_DIR)
            category, subcat = get_category_subcategory(rel_path)
            
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            title = data.get('title', fpath.stem)
            chars = data.get('characters', [])
            content = data.get('content', [])
            source_url = data.get('source_url', '')
            crawled_at = data.get('crawled_at', '')
            wikitext = data.get('raw_wikitext', '')
            
            # Story row
            story_batch.append((
                title, category, subcat, chars,
                json.dumps(content, ensure_ascii=False) if content else None,
                wikitext or None, source_url or None, crawled_at or None,
                str(rel_path)
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
                
                dialogue_batch.append((
                    title, category, speaker or '(旁白)', text,
                    dtype, emotion or None, idx
                ))
            
            # Insert in batches
            if len(story_batch) >= 100:
                cur.executemany(
                    """INSERT INTO story_pages 
                    (title, category, sub_category, characters, content_json, raw_wikitext, source_url, crawled_at, json_file)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    story_batch
                )
                story_batch.clear()
            
            if len(dialogue_batch) >= 500:
                cur.executemany(
                    """INSERT INTO dialogues 
                    (story_title, category, speaker, text, dialogue_type, emotion, line_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    dialogue_batch
                )
                dialogue_batch.clear()
                
        except Exception as e:
            errors.append((str(fpath), str(e)))
            continue
    
    # Final batch inserts
    if story_batch:
        cur.executemany(
            """INSERT INTO story_pages 
            (title, category, sub_category, characters, content_json, raw_wikitext, source_url, crawled_at, json_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            story_batch
        )
    
    if dialogue_batch:
        cur.executemany(
            """INSERT INTO dialogues 
            (story_title, category, speaker, text, dialogue_type, emotion, line_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            dialogue_batch
        )
    
    # Commit story and dialogue inserts
    conn.commit()
    
    # Update character profiles
    print("Updating character profiles...")
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
    cur.close()
    conn.close()
    
    total_time = time.time() - start
    print(f"\n=== DONE ===")
    print(f"Time: {total_time:.1f}s")
    print(f"Files processed: {total - len(errors)}/{total}")
    if errors:
        print(f"Errors: {len(errors)}")
        for fp, err in errors[:5]:
            print(f"  {fp}: {err}")
    
    # Quick stats
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM story_pages")
    story_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dialogues")
    dialogue_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM character_profiles")
    char_cnt = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    print(f"\nDatabase counts:")
    print(f"  story_pages: {story_cnt}")
    print(f"  dialogues: {dialogue_cnt}")
    print(f"  character_profiles: {char_cnt}")

if __name__ == "__main__":
    main()
