import sqlite3

conn = sqlite3.connect("agent_skills_release.db")
print("connected")

rows = conn.execute("""
    SELECT file_sha, COUNT(*) AS copies
    FROM artifacts
    GROUP BY file_sha
    ORDER BY copies DESC
    LIMIT 20
""")
for sha, copies in rows:
    print(copies, sha[:12])
    
rows = conn.execute("""
    WITH c AS (
      SELECT file_sha, COUNT(*) AS n FROM artifacts GROUP BY file_sha
    )
    SELECT
      CASE
        WHEN n = 1 THEN '1'
        WHEN n <= 5 THEN '2-5'
        WHEN n <= 20 THEN '6-20'
        WHEN n <= 100 THEN '21-100'
        ELSE '100+'
      END AS bucket,
      COUNT(*) AS skills
    FROM c
    GROUP BY bucket
""")
for bucket, skills in rows:
    print(bucket, skills)
