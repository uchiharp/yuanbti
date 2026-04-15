#!/usr/bin/env python3
"""补导 dialogues 到 db9"""

import json
import sys
import psycopg2
from pathlib import Path

DATA_DIR = Path(__file__).parent
DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

DIR_MAP = {
    "密探/传唤": "密探传唤", "密探/故事": "密探故事", "密探/留音": "密探留音", "密探/羁绊": "密探羁绊",
    "剧情/主线": "主线剧情", "剧情/活动": "活动剧情", "剧情/恋念": "恋念剧情",
    "男主/红鸾花笺": "红鸾花笺", "男主/恋念之音": "恋念之音", "男主/约会": "约会", "男主/留音": "男主留音",
    "鸢记": "鸢记",
}

def main():
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()

    json_files = sorted(DATA_DIR.rglob("*.json"))
    json_files = [f for f in json_files if any(f.relative_to(DATA_DIR).parts[0] in d for d in DIR_MAP)]
    print(f"Found {len(json_files)} files")

    batch = []
    total = 0
    errors = 0

    for i, fpath in enumerate(json_files):
        try:
            rel = fpath.relative_to(DATA_DIR)
            parts = rel.parts
            category = DIR_MAP.get(parts[0], parts[0])

            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            title = data.get('title', fpath.stem)
            content = data.get('content', [])

            for idx, item in enumerate(content):
                if not isinstance(item, dict):
                    continue
                dtype = item.get('type', 'raw')
                speaker = item.get('speaker', '(旁白)') or '(旁白)'
                text = item.get('text', '')
                emotion = item.get('emotion', '')
                batch.append((title, category, speaker, text, dtype, emotion, idx))

                if len(batch) >= 1000:
                    cur.executemany(
                        "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        batch
                    )
                    total += len(batch)
                    batch.clear()
                    conn.commit()
                    if total % 10000 < 1000:
                        print(f"  {i+1}/{len(json_files)} files, {total} dialogues")

        except Exception as e:
            errors += 1
            conn.rollback()

    # Flush remaining
    if batch:
        cur.executemany(
            "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            batch
        )
        total += len(batch)
        conn.commit()

    cur.close()
    conn.close()
    print(f"\nDone! Total: {total} dialogues, errors: {errors}")

if __name__ == "__main__":
    main()
