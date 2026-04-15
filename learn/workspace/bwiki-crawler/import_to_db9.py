#!/usr/bin/env python3
"""Import BWIKI 代号鸢 crawled data into db9 (learn_test database)."""

import json
import os
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent
DB_NAME = "learn_test"
DB9_CLI = "/Users/sunwenyong/.local/bin/db9"

# Directory → (category, sub_category) mapping
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


def get_db_url():
    """Get db9 connection string from file, CLI arg, or db9 CLI."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    url_file = Path(__file__).parent / "db_url.txt"
    if url_file.exists():
        for line in url_file.read_text().splitlines():
            if "postgresql://" in line:
                return line.strip()
    url = os.environ.get('DB9_URL')
    if url:
        return url
    result = subprocess.run(
        [DB9_CLI, "db", "connect", DB_NAME],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.splitlines():
        if "postgresql://" in line:
            return line.strip()
    # Also check stderr
    for line in result.stderr.splitlines():
        if "postgresql://" in line:
            return line.strip()
    raise RuntimeError(f"Cannot get db URL. stdout: {result.stdout[:500]}\nstderr: {result.stderr[:500]}")


def get_category_subcategory(rel_path: Path):
    """Infer category and sub_category from relative path."""
    parts = rel_path.parts
    # Try matching top-level directories
    for key in sorted(DIR_MAP.keys(), key=len, reverse=True):
        key_parts = key.split("/")
        if len(parts) >= len(key_parts) and parts[:len(key_parts)] == tuple(key_parts):
            return DIR_MAP[key]
    # Fallback: use first dir as category
    return (parts[0] if parts else "unknown", "/".join(parts[:2]) if len(parts) >= 2 else parts[0] if parts else "unknown")


def main():
    import psycopg2

    db_url = get_db_url()
    conn = psycopg2.connect(db_url)
    conn.autocommit = False
    cur = conn.cursor()

    # Collect all JSON files
    json_files = sorted(DATA_DIR.rglob("*.json"))
    print(f"Found {len(json_files)} JSON files")

    errors = []
    story_count = 0
    dialogue_count = 0
    char_story_counts = {}  # name -> story_count
    char_dialogue_counts = {}  # name -> dialogue_count

    # Batch buffers
    story_batch = []
    dialogue_batch = []
    BATCH_SIZE = 500

    def flush_stories():
        nonlocal story_count
        if not story_batch:
            return
        rows = []
        for r in story_batch:
            rows.append((
                r['title'], r['category'], r['sub_category'],
                r['characters'], r['content_json'], r['raw_wikitext'],
                r['source_url'], r['crawled_at'], r['json_file']
            ))
        cur.executemany(
            """INSERT INTO story_pages (title, category, sub_category, characters, content_json, raw_wikitext, source_url, crawled_at, json_file)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            rows
        )
        story_count += len(rows)
        story_batch.clear()
        conn.commit()
        print(f"  Stories committed: {story_count}")

    def flush_dialogues():
        nonlocal dialogue_count
        if not dialogue_batch:
            return
        cur.executemany(
            """INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            dialogue_batch
        )
        dialogue_count += len(dialogue_batch)
        dialogue_batch.clear()
        conn.commit()

    for fpath in json_files:
        try:
            rel_path = fpath.relative_to(DATA_DIR)
            category, sub_category = get_category_subcategory(rel_path)

            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            title = data.get('title', fpath.stem)
            characters = data.get('characters', [])
            content = data.get('content', [])
            source_url = data.get('source_url', '')
            crawled_at = data.get('crawled_at', '')
            raw_wikitext = data.get('raw_wikitext', '')

            # Build story_pages row
            story_batch.append({
                'title': title,
                'category': category,
                'sub_category': sub_category,
                'characters': characters,
                'content_json': json.dumps(content, ensure_ascii=False) if content else None,
                'raw_wikitext': raw_wikitext or None,
                'source_url': source_url or None,
                'crawled_at': crawled_at or None,
                'json_file': str(rel_path),
            })

            # Track character story appearances
            for ch in characters:
                char_story_counts[ch] = char_story_counts.get(ch, 0) + 1

            # Build dialogue rows
            for idx, item in enumerate(content):
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
                    dtype, emotion or None, idx
                ))

                if len(dialogue_batch) >= BATCH_SIZE:
                    flush_dialogues()

            if len(story_batch) >= 100:
                flush_stories()

        except Exception as e:
            errors.append((str(fpath), str(e)))
            continue

    # Flush remaining
    flush_dialogues()
    flush_stories()

    # Update character_profiles
    print("Updating character_profiles...")
    all_chars = set(char_story_counts.keys()) | set(char_dialogue_counts.keys())
    for name in all_chars:
        sc = char_story_counts.get(name, 0)
        dc = char_dialogue_counts.get(name, 0)
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

    print(f"\n=== Import Complete ===")
    print(f"Stories: {story_count}")
    print(f"Dialogues: {dialogue_count}")
    print(f"Unique characters: {len(all_chars)}")
    if errors:
        print(f"Errors: {len(errors)}")
        for fp, err in errors[:10]:
            print(f"  {fp}: {err}")
    print("Done!")


if __name__ == "__main__":
    main()
