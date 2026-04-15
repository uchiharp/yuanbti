#!/usr/bin/env python3
"""从本地 JSON 文件读取 + psycopg2 COPY 协议写入，最快方案"""
import psycopg2, json, csv, io
from pathlib import Path

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"
DATA_DIR = Path(__file__).parent

DIR_MAP = {
    "密探/传唤": "密探传唤", "密探/故事": "密探故事", "密探/留音": "密探留音", "密探/羁绊": "密探羁绊",
    "剧情/主线": "主线剧情", "剧情/活动": "活动剧情", "剧情/恋念": "恋念剧情",
    "男主/红鸾花笺": "红鸾花笺", "男主/恋念之音": "恋念之音", "男主/约会": "约会", "男主/留音": "男主留音",
    "鸢记": "鸢记",
}

# 收集所有 JSON 文件
json_files = sorted(DATA_DIR.rglob("*.json"))
json_files = [f for f in json_files if any(f.relative_to(DATA_DIR).parts[0] in d for d in DIR_MAP)]
print(f"Found {len(json_files)} JSON files", flush=True)

# 从 JSON 构建 CSV 数据
buf = io.StringIO()
writer = csv.writer(buf, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
total_rows = 0

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
        speaker = item.get('speaker', '(旁白)') or '(旁白)'
        text = item.get('text', '')
        dtype = item.get('type', 'raw')
        emotion = item.get('emotion', '')
        # 转义 tab 和 newline
        writer.writerow([title, category, speaker, text, dtype, emotion, idx])
        total_rows += 1
    
    if total_rows % 10000 < 50:
        print(f"  Parsed: {json_files.index(fpath)+1}/{len(json_files)} files, {total_rows} rows", flush=True)

buf.seek(0)
print(f"\nTotal rows to insert: {total_rows}", flush=True)

# 清空 + COPY 写入
conn = psycopg2.connect(DB_URL, connect_timeout=60)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SET db9.dml_table_scan_max_rows = 0")

print("Clearing...", flush=True)
cur.execute("DELETE FROM dialogues")
print("  Cleared", flush=True)

# 用 COPY
print("Copying via psycopg2...", flush=True)
cur.copy_expert(
    "COPY dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order) FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '')",
    buf
)
print(f"  Copied!", flush=True)

# 验证
cur.execute("SELECT COUNT(*) FROM dialogues")
d = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
s = cur.fetchone()[0]
print(f"\nFinal: {d} dialogues from {s} stories", flush=True)

conn.close()
print("Done!", flush=True)
