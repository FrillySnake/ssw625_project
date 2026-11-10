import sqlite3

conn = sqlite3.connect("agent_skills_release.db")
print("connected")

tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
for row in tables:
    print(row[0])
total = conn.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]
print("total artifact rows:", total, "(expected ~)")

primaries = conn.execute("SELECT COUNT(*) FROM artifacts WHERE dedup_primary = 1").fetchone()[0]
print("distinct contents:", primaries, "(expected ~)")
