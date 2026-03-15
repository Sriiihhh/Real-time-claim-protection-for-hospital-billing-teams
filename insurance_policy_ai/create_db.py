import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS policies(
id TEXT PRIMARY KEY,
policy_name TEXT,
company TEXT,
status TEXT
)
""")

conn.commit()
conn.close()

print("Database ready!")