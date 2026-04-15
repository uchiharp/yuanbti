#!/usr/bin/env python3
"""从本地 JSON 读取 + executemany 批量写入（自动重试）"""
import psycopg2, json, time, sys
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
print(f"Found {len(json_files)} JSON files", flush=True)

# 先读取所有数据到内存
all_rows = []
for fpath in json_files:
    rel = fpath.relative_to(DATA_DIR)
    parts = rel.parts
    category = DIR_MAP.get(parts[0], parts[0])
    
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    title = data.get('title', fpath.stem)
    content = data.get('content', [])
    
    for idx, item in enumerate(content):
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

print(f"Total rows: {len(all_rows)}", flush=True)

# 连接 + 清空
conn = psycopg2.connect(DB_URL, connect_timeout=60)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SET db9.dml_table_scan_max_rows = 0")
print("Clearing...", flush=True)
cur.execute("DELETE FROM dialogues")
print("  Cleared", flush=True)

# 批量写入，每次 INSERT_SIZE 条
INSERT_SIZE = 200
total_inserted = 0
errors = 0

for i in range(0, len(all_rows), INSERT_SIZE):
    chunk = all_rows[i:i+INSERT_SIZE]
    try:
        conn.autocommit = False
        cur.executemany(
            "INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            chunk
        )
        conn.commit()
        total_inserted += len(chunk)
        conn.autocommit = True
    except Exception as e:
        conn.autocommit = True
        errors += 1
        if errors <= 3:
            print(f"  Error at {i}: {e}", flush=True)
        time.sleep(0.5)
    
    if total_inserted % 5000 < INSERT_SIZE:
        print(f"  Progress: {total_inserted}/{len(all_rows)} ({total_inserted*100//len(all_rows)}%)", flush=True)

print(f"\nInserted: {total_inserted}, Errors: {errors}", flush=True)

# 验证
cur.execute("SELECT COUNT(*) FROM dialogues")
d = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
s = cur.fetchone()[0]
print(f"Final: {d} dialogues from {s} stories", flush=True)

conn.close()
