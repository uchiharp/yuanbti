#!/usr/bin/env python3
"""execute_values + 小批量 + 进度追踪"""
import psycopg2, json, time
from psycopg2.extras import execute_values
from pathlib import Path

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"
DATA_DIR = Path(__file__).parent

DIR_MAP = {
    "密探/传唤": "密探传唤", "密探/故事": "密探故事", "密探/留音": "密探留音", "密探/羁绊": "密探羁绊",
    "剧情/主线": "主线剧情", "剧情/活动": "活动剧情", "剧情/恋念": "恋念剧情",
    "男主/红鸾花笺": "红鸾花笺", "男主/恋念之音": "恋念之音", "男主/约会": "约会", "男主/留音": "男主留音",
    "鸢记": "鸢记",
}

json_files = sorted(DATA_DIR.rglob("*.json"))
json_files = [f for f in json_files if any(f.relative_to(DATA_DIR).parts[0] in d for d in DIR_MAP)]
print(f"Files: {len(json_files)}", flush=True)

# 读取所有数据
all_rows = []
for fpath in json_files:
    rel = fpath.relative_to(DATA_DIR)
    parts = rel.parts
    category = DIR_MAP.get(parts[0], parts[0])
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    title = data.get('title', fpath.stem)
    for idx, item in enumerate(data.get('content', [])):
        if not isinstance(item, dict) or not item.get('type'):
            continue
        all_rows.append((
            title, category,
            item.get('speaker') or '(旁白)',
            item.get('text', ''),
            item.get('type', 'raw'),
            item.get('emotion', ''),
            idx
        ))

print(f"Rows: {len(all_rows)}", flush=True)

# 连接
conn = psycopg2.connect(DB_URL, connect_timeout=60)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SET db9.dml_table_scan_max_rows = 0")

# 清空
print("Clearing...", flush=True)
cur.execute("DELETE FROM dialogues")
print("  Done", flush=True)

# execute_values 批量写入
CHUNK = 100  # 每次 100 条
total = 0
start = time.time()

for i in range(0, len(all_rows), CHUNK):
    chunk = all_rows[i:i+CHUNK]
    try:
        conn.autocommit = False
        execute_values(
            cur,
            "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES %s",
            chunk,
            page_size=CHUNK
        )
        conn.commit()
        conn.autocommit = True
        total += len(chunk)
    except Exception as e:
        conn.autocommit = True
        print(f"  Error at {i}: {e}", flush=True)
        time.sleep(1)
    
    if total % 1000 < CHUNK or i + CHUNK >= len(all_rows):
        elapsed = time.time() - start
        rate = total / elapsed if elapsed > 0 else 0
        remaining = (len(all_rows) - total) / rate if rate > 0 else 0
        print(f"  {total}/{len(all_rows)} ({total*100//len(all_rows)}%) {rate:.0f}/s ETA {remaining:.0f}s", flush=True)

# 统计
cur.execute("SELECT COUNT(*) FROM dialogues")
d = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
s = cur.fetchone()[0]
elapsed = time.time() - start
print(f"\nDone! {d} dialogues, {s} stories in {elapsed:.0f}s", flush=True)

conn.close()
