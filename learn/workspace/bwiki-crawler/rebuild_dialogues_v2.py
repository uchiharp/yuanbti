#!/usr/bin/env python3
"""用 SQL jsonb_array_elements + 子查询序号直接插入 dialogues"""
import psycopg2

DB_URL = "postgresql://rlyuwmobltkt.importer:importer2026@pg.db9.io:5433/postgres"

conn = psycopg2.connect(DB_URL, connect_timeout=30)
conn.autocommit = False
cur = conn.cursor()

# 先看下 PostgreSQL 版本和 WITH ORDINALITY 支持
print("Testing WITH ORDINALITY support...", flush=True)
try:
    cur.execute("""
        SELECT 1 FROM story_pages sp
        CROSS JOIN jsonb_array_elements(sp.content_json) WITH ORDINALITY AS t(elem, i)
        LIMIT 1
    """)
    has_ordinality = True
    print("  Supported!", flush=True)
except Exception as e:
    has_ordinality = False
    print(f"  Not supported: {e}", flush=True)

# 清空重建（比增量去重更简单可靠）
print("Clearing existing dialogues...", flush=True)
cur.execute("DELETE FROM dialogues")
conn.commit()
print("  Cleared", flush=True)

# 全量插入
print("Inserting all dialogues via SQL...", flush=True)
if has_ordinality:
    sql = """
        INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
        SELECT 
            sp.title,
            sp.category,
            COALESCE(elem->>'speaker', '(旁白)'),
            COALESCE(elem->>'text', ''),
            COALESCE(elem->>'type', 'raw'),
            COALESCE(elem->>'emotion', ''),
            i - 1
        FROM story_pages sp
        CROSS JOIN jsonb_array_elements(sp.content_json) WITH ORDINALITY AS t(elem, i)
        WHERE sp.content_json IS NOT NULL
        AND jsonb_typeof(elem) = 'object'
        AND elem->>'type' IS NOT NULL
    """
else:
    # 不带序号的版本
    sql = """
        INSERT INTO dialogues (story_title, category, speaker, text, dialogue_type, emotion, line_order)
        SELECT 
            sp.title,
            sp.category,
            COALESCE(elem->>'speaker', '(旁白)'),
            COALESCE(elem->>'text', ''),
            COALESCE(elem->>'type', 'raw'),
            COALESCE(elem->>'emotion', ''),
            0
        FROM story_pages sp, jsonb_array_elements(sp.content_json) elem
        WHERE sp.content_json IS NOT NULL
        AND jsonb_typeof(elem) = 'object'
        AND elem->>'type' IS NOT NULL
    """

cur.execute(sql)
conn.commit()
print(f"  Inserted: {cur.rowcount} rows", flush=True)

# 验证
cur.execute("SELECT COUNT(*) FROM dialogues")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
stories = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM story_pages")
sp_total = cur.fetchone()[0]
print(f"\nResult: {total} dialogues from {stories}/{sp_total} stories", flush=True)

conn.close()
print("Done!", flush=True)
