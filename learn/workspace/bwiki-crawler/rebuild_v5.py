#!/usr/bin/env python3
"""分批小量插入 dialogues"""
import psycopg2

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

conn = psycopg2.connect(DB_URL, connect_timeout=30)
conn.autocommit = True
cur = conn.cursor()

# 调大限制 + 超时
cur.execute("SET db9.dml_table_scan_max_rows = 0")
cur.execute("SET statement_timeout = '300000'")  # 5min

# 清空
print("Clearing...", flush=True)
cur.execute("DELETE FROM dialogues")
print("  Cleared", flush=True)

# 小批量
BATCH = 50
offset = 0
total = 0

while True:
    try:
        cur.execute("""
            INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
            SELECT 
                sp.title, sp.category,
                COALESCE(elem->>'speaker', '(旁白)'),
                COALESCE(elem->>'text', ''),
                COALESCE(elem->>'type', 'raw'),
                COALESCE(elem->>'emotion', ''),
                0
            FROM (
                SELECT title, category, content_json 
                FROM story_pages 
                WHERE content_json IS NOT NULL 
                ORDER BY title LIMIT %s OFFSET %s
            ) sp, jsonb_array_elements(sp.content_json) elem
            WHERE jsonb_typeof(elem) = 'object' AND elem->>'type' IS NOT NULL
        """, (BATCH, offset))
        
        inserted = cur.rowcount
        print(f"  offset={offset}: +{inserted} (total: {total+inserted})", flush=True)
        total += inserted
        offset += BATCH
        if inserted == 0:
            break
    except Exception as e:
        print(f"  Error at offset {offset}: {e}", flush=True)
        conn.rollback()
        break

print(f"\nInserted: {total}", flush=True)

# 补 line_order（逐 story 更新）
print("Fixing line_order...", flush=True)
conn.autocommit = False
cur.execute("SELECT DISTINCT story_title FROM dialogues ORDER BY story_title")
titles = [r[0] for r in cur.fetchall()]
fixed = 0
for title in titles:
    cur.execute("SELECT id FROM dialogues WHERE story_title = %s ORDER BY id", (title,))
    ids = [r[0] for r in cur.fetchall()]
    for i, did in enumerate(ids):
        cur.execute("UPDATE dialogues SET line_order = %s WHERE id = %s", (i, did))
    fixed += 1
    if fixed % 200 == 0:
        conn.commit()
        print(f"  {fixed}/{len(titles)}", flush=True)
conn.commit()

# 统计
cur.execute("SELECT COUNT(*) FROM dialogues")
d = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
s = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM story_pages")
sp = cur.fetchone()[0]
print(f"\nFinal: {d} dialogues, {s}/{sp} stories", flush=True)

conn.close()
print("Done!", flush=True)
