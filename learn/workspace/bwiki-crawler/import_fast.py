#!/usr/bin/env python3
"""Import BWIKI data into db9 using persistent credentials and COPY for speed."""

import json
import os
import sys
import psycopg2
from pathlib import Path
from io import StringIO

DATA_DIR = Path(__file__).parent
DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

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


def get_category(rel_path: Path):
    parts = rel_path.parts
    for key in sorted(DIR_MAP.keys(), key=len, reverse=True):
        key_parts = key.split("/")
        if len(parts) >= len(key_parts) and parts[:len(key_parts)] == tuple(key_parts):
            return DIR_MAP[key]
    return (parts[0] if parts else "unknown", str(rel_path.parent))


def main():
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # Clear old data
    print("Clearing old data...")
    cur.execute("DELETE FROM story_pages")
    cur.execute("DELETE FROM dialogues")
    cur.execute("DELETE FROM character_profiles")

    json_files = sorted(DATA_DIR.rglob("*.json"))
    # Filter: only files in known subdirectories
    json_files = [f for f in json_files if any(f.relative_to(DATA_DIR).parts[0] in d for d in DIR_MAP)]
    print(f"Found {len(json_files)} JSON files to import")

    story_buf = StringIO()
    dialogue_buf = StringIO()
    story_count = 0
    dialogue_count = 0
    errors = []

    for i, fpath in enumerate(json_files):
        try:
            rel = fpath.relative_to(DATA_DIR)
            category, sub_category = get_category(rel)

            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            title = data.get('title', fpath.stem)
            characters = data.get('characters', [])
            content = data.get('content', [])
            source_url = data.get('source_url', '')
            crawled_at = data.get('crawled_at', '')
            raw_wikitext = data.get('raw_wikitext', '')
            content_json = json.dumps(content, ensure_ascii=False) if content else ''

            # Escape for CSV
            def esc(s):
                if s is None: return ''
                s = str(s).replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '').replace('\t', '\\t')
                if ',' in s or '"' in s:
                    return '"' + s.replace('"', '""') + '"'
                return s

            # Story row
            story_buf.write(f"{esc(title)}\t{esc(category)}\t{esc(sub_category)}\t{esc(json.dumps(characters, ensure_ascii=False))}\t{esc(content_json)}\t{esc(raw_wikitext)}\t{esc(source_url)}\t{esc(crawled_at)}\t{esc(str(rel))}\n")
            story_count += 1

            # Dialogue rows
            for idx, item in enumerate(content):
                if not isinstance(item, dict):
                    continue
                dtype = item.get('type', 'raw')
                speaker = item.get('speaker', '(旁白)')
                text = item.get('text', '')
                emotion = item.get('emotion', '')
                dialogue_buf.write(f"{esc(title)}\t{esc(category)}\t{esc(speaker)}\t{esc(text)}\t{esc(dtype)}\t{esc(emotion)}\t{idx}\n")
                dialogue_count += 1

            # Flush every 500 files
            if (i + 1) % 500 == 0:
                print(f"  Progress: {i+1}/{len(json_files)} files, {story_count} stories, {dialogue_count} dialogues")

        except Exception as e:
            errors.append((str(fpath), str(e)))

    # Flush remaining
    story_data = story_buf.getvalue()
    dialogue_data = dialogue_buf.getvalue()
    story_buf.close()
    dialogue_buf.close()

    print(f"\nImporting {story_count} stories via COPY...")
    if story_data:
        cur.copy_expert("""
            COPY story_pages (title, category, sub_category, characters, content_json, raw_wikitext, source_url, crawled_at, json_file)
            FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '')
        """, StringIO(story_data))

    print(f"Importing {dialogue_count} dialogues via COPY...")
    if dialogue_data:
        cur.copy_expert("""
            COPY dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
            FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '')
        """, StringIO(dialogue_data))

    # Update character_profiles
    print("Updating character_profiles...")
    cur.execute("""
        INSERT INTO character_profiles (name, story_count, dialogue_count)
        SELECT 
            unnest(characters) as name,
            1 as story_count,
            0 as dialogue_count
        FROM story_pages
        ON CONFLICT (name) DO UPDATE SET 
            story_count = character_profiles.story_count + 1
    """)
    cur.execute("""
        INSERT INTO character_profiles (name, story_count, dialogue_count)
        SELECT 
            speaker as name,
            0 as story_count,
            COUNT(*) as dialogue_count
        FROM dialogues
        WHERE speaker != '(旁白)' AND dialogue_type = 'dialogue'
        GROUP BY speaker
        ON CONFLICT (name) DO UPDATE SET 
            dialogue_count = character_profiles.dialogue_count + EXCLUDED.dialogue_count
    """)

    print(f"\n=== Import Complete ===")
    print(f"Stories: {story_count}")
    print(f"Dialogues: {dialogue_count}")
    if errors:
        print(f"Errors: {len(errors)}")
        for fp, err in errors[:10]:
            print(f"  {fp}: {err}")

    cur.close()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
