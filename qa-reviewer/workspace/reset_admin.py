#!/usr/bin/env python3
import sqlite3
import bcrypt
import sys

db_path = "/Users/sunwenyong/projects/openclaw-hub/backend/data/hub.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 生成密码admin的bcrypt哈希
password = "admin"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

cur.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
conn.commit()
print(f"Updated admin password to 'admin'")
cur.close()
conn.close()