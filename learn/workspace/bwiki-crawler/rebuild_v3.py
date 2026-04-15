#!/usr/bin/env python3
"""用 SQL 直接插入 dialogues（无 WITH ORDINALITY，分批处理）"""
import psycopg2

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

conn = psycopg2.connect(DB_URL, connect_timeout=30)
conn.autocommit = True  # 每条语句自动提交
cur = conn.cursor()

# 清空重建
print("Clearing existing dialogues...", flush=True)
cur.execute("DELETE FROM dialogues")
print("  Cleared", flush=True)

# 分批插入（每批 500 个 story）
BATCH = 500
offset = 0

while True:
    cur.execute(
        "SELECT COUNT(*) FROM story_pages WHERE content_json IS NOT NULL"
    )
    total_stories = cur.fetchone()[0]
    
    cur.execute("""
        INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
        SELECT 
            sp.title,
            sp.category,
            COALESCE(elem->>'speaker', '(旁白)'),
            COALESCE(elem->>'text', ''),
            COALESCE(elem->>'type', 'raw'),
            COALESCE(elem->>'emotion', ''),
            0
        FROM (
            SELECT title, category, content_json 
            FROM story_pages 
            WHERE content_json IS NOT NULL 
            ORDER BY title
            LIMIT %s OFFSET %s
        ) sp, jsonb_array_elements(sp.content_json) elem
        WHERE jsonb_typeof(elem) = 'object'
        AND elem->>'type' IS NOT NULL
    """, (BATCH, offset))
    
    inserted = cur.rowcount
    print(f"  Batch offset={offset}: inserted {inserted}", flush=True)
    
    offset += BATCH
    if inserted == 0:
        break

# 后续用 Python 补上 line_order
print("\nFixing line_order...", flush=True)
conn.autocommit = False
cur.execute("SELECT DISTINCT story_title FROM dialogues ORDER BY story_title")
all_titles = [r[0] for r in cur.fetchall()]
print(f"  {len(all_titles)} stories to fix", flush=True)

fixed = 0
for title in all_titles:
    cur.execute("""
        SELECT id FROM dialogues 
        WHERE story_title = %s 
        ORDER BY id
    """, (title,))
    ids = [r[0] for r in cur.fetchall()]
    for i, did in enumerate(ids):
        cur.execute("UPDATE dialogues SET line_order = %s WHERE id = %s", (i, did))
    fixed += 1
    if fixed % 100 == 0:
        conn.commit()
        print(f"  Fixed line_order: {fixed}/{len(all_titles)}", flush=True)
conn.commit()

# 最终统计
cur.execute("SELECT COUNT(*) FROM dialogues")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
stories = cur.fetchone()[0]
print(f"\nFinal: {total} dialogues from {stories}/{total_stories} stories", flush=True)

conn.close()
print("Done!", flush=True)
