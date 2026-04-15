#!/usr/bin/env python3
"""用 admin 连接直接 SQL 拆分 story_pages → dialogues"""
import psycopg2

ADMIN_URL = "postgresql://rlyuwmobltkt.admin:eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6InByb2QtMSJ9.eyJpc3MiOiJodHRwczovL2FwaS5kYjkuYWkiLCJhdWQiOiJkYjktc2VydmVyIiwiZXhwIjoxNzc2MDEyNDI2LCJpYXQiOjE3NzYwMTE4MjYsImp0aSI6ImI2ODg2MTE2LTAxOWYtNGM0Zi1hMTA0LTM3MTAwNGQ5NzIyNiIsInNjcCI6ImRiOmNvbm5lY3QiLCJ0aWQiOiJybHl1d21vYmx0a3QiLCJ1c3IiOiJybHl1d21vYmx0a3QuYWRtaW4iLCJzdWIiOiJhZDA0MjY0Yy02NmFkLTQ2OTItYWViMy04NWY5ZjlkOTUzMjMiLCJidWRnZXRfb3duZXJfaWQiOiJybHl1d21vYmx0a3QiLCJidWRnZXRfcnBzIjoxMDAsImJ1ZGdldF9idXJzdCI6MjAwLCJidWRnZXRfdGltZW91dF9tcyI6MzAwMDAsImJ1ZGdldF9tYXhfY29uY3VycmVudCI6MTB9.Kb1kpWIrXxR2ntSlW7ygEBYe_eZqhJxXWpD-Qi3EeyNh41DsXIo-cSvQq62oZumH22_X2oXzkRymPxiaWOn3Ghamkq3P6pciBZ3jMEGnYSNQhgYNw1T08JIHvAde9r2aEhkPcEb9nsMOwvzSo-vn-PoKrWz5MSpf-Ft1XSV8AAGTj-2-cZrm2UXiNdeNAXg90e-ayHrMyi0mvNMcXLfksxYa_aYFHFvH9gboJatSDYJt-8D__t3X7CibyJ1WNnpqb1iDYlthl12L3osMzmXPXHQeATr10ocsd8koxg7MdvPVuxCAaBY2a1BpxeO9MyNUKBL-R89P8Va_Abhcg2bK3A@pg.db9.io:5433/postgres"

conn = psycopg2.connect(ADMIN_URL, connect_timeout=30)
conn.autocommit = False
cur = conn.cursor()

# 检查 WITH ORDINALITY 支持
print("Testing WITH ORDINALITY...", flush=True)
try:
    cur.execute("""
        SELECT 1 FROM story_pages sp
        CROSS JOIN jsonb_array_elements(sp.content_json) WITH ORDINALITY AS t(elem, i)
        LIMIT 1
    """)
    print("  WITH ORDINALITY works!", flush=True)
except Exception as e:
    print(f"  WITH ORDINALITY not supported: {e}", flush=True)
    conn.close()
    exit(1)

# 步骤1：清空现有 dialogues，重建
print("Step 1: Clear existing dialogues...", flush=True)
cur.execute("DELETE FROM dialogues")
conn.commit()
print("  Cleared", flush=True)

# 步骤2：用 SQL 直接拆分插入
print("Step 2: Insert all dialogues from story_pages...", flush=True)
cur.execute("""
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
""")
conn.commit()
print(f"  Inserted: {cur.rowcount} rows", flush=True)

# 步骤3：验证
cur.execute("SELECT COUNT(*) FROM dialogues")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT story_title) FROM dialogues")
stories = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM story_pages")
sp_total = cur.fetchone()[0]
print(f"\nResult: {total} dialogues from {stories}/{sp_total} stories", flush=True)

conn.close()
print("Done!", flush=True)
