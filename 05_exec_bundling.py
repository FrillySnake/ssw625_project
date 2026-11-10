import sqlite3
conn = sqlite3.connect("agent_skills_release.db")

total = conn.execute("SELECT COUNT(*) FROM artifacts WHERE dedup_primary = 1 AND content_fetched = 1").fetchone()[0]
with_execs = conn.execute("""
    SELECT COUNT(DISTINCT a.path), COUNT(DISTINCT a.repo_full_name)
    FROM artifacts a
    JOIN artifact_siblings s
        ON a.repo_full_name = s.repo_full_name
        AND a.path = s.artifact_path
    WHERE a.dedup_primary = 1
        AND a.content_fetched = 1
        AND s.entry_type = 'file'
        AND (
            LOWER(s.entry_name) LIKE '%.exe'
            OR LOWER(s.entry_name) LIKE '%.dll'
            OR LOWER(s.entry_name) LIKE '%.so'
            OR LOWER(s.entry_name) LIKE '%.bin'
            OR LOWER(s.entry_name) LIKE '%.elf'
            OR LOWER(s.entry_name) LIKE '%.dylib'
            OR LOWER(s.entry_name) LIKE '%.com')
""").fetchone()
print(f"found {with_execs[0]} skills across {with_execs[1]} repos bundling potential executable files out of {total} skills")

temp = "JOIN artifacts r ON r.file_sha = a.file_sha AND r.dedup_primary = 1 AND r.has_scripts = 1"

rows = conn.execute("""
    SELECT a.file_sha, COUNT(*) AS copies
    FROM artifacts a
    JOIN artifact_siblings s
            ON a.repo_full_name = s.repo_full_name
            AND a.path = s.artifact_path
        WHERE a.dedup_primary = 1
            AND a.content_fetched = 1
            AND s.entry_type = 'file'
            AND (
                LOWER(s.entry_name) LIKE '%.exe'
                OR LOWER(s.entry_name) LIKE '%.dll'
                OR LOWER(s.entry_name) LIKE '%.so'
                OR LOWER(s.entry_name) LIKE '%.bin'
                OR LOWER(s.entry_name) LIKE '%.elf'
                OR LOWER(s.entry_name) LIKE '%.dylib'
                OR LOWER(s.entry_name) LIKE '%.com')
    GROUP BY a.file_sha
    ORDER BY copies DESC
    LIMIT 5
""").fetchall()
for sha, copies in rows:
    print(copies, sha[:12])