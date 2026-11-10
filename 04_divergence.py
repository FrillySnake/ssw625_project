import sqlite3, csv, re

EXEC_PATTERNS = {
    "curl": r"(?<![\w-])curl(?![\w-])",
    "wget": r"(?<![\w-])wget(?![\w-])",
    "chmod": r"\bchmod\s+\+x\b",
    "eval": r"\beval\s*\(",
    "exec": r"\bexec\s*\(",
    "subprocess": r"\bsubprocess\b",
    "os.system": r"\bos\s*\.\s*system\s*\(",
}

NET_PATTERNS = {
    "http": r"https?://",
    "fetch": r"\bfetch\s*\(",
    "requests": r"\brequests\s*\.",
}

def detect_tokens(text, tokens):
    found = set()

    for name, pattern in tokens.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.add(name)

    return found


def new_tokens(old_text, new_text, tokens):
    old_found = detect_tokens(old_text, tokens)
    new_found = detect_tokens(new_text, tokens)

    return new_found - old_found

conn = sqlite3.connect("agent_skills_release.db")
rows = conn.execute("""
    SELECT file_sha, content FROM artifacts
    WHERE content_fetched = 1 AND content IS NOT NULL
""").fetchall()

pairs = []
with open("pairs.csv") as f:
    for row in csv.DictReader(f):
        pairs.append((int(row["i"]), int(row["j"]), float(row["score"])))
print("pairs loaded:", len(pairs))

exec_pairs = 0
net_pairs = 0
examples = []

for i, j, s in pairs:
    a = rows[i][1]
    b = rows[j][1]
    exec_new = new_tokens(a, b, EXEC_PATTERNS) | new_tokens(b, a, EXEC_PATTERNS)
    net_new = new_tokens(a, b, NET_PATTERNS) | new_tokens(b, a, NET_PATTERNS)
    if exec_new:
        exec_pairs += 1
    if net_new:
        net_pairs += 1
    if (exec_new or net_new) and len(examples) < 5:
        examples.append((rows[i][0][:8], rows[j][0][:8], sorted(exec_new), sorted(net_new)))

print("pairs with new command execution:", exec_pairs, "of", len(pairs))
print("pairs with new network access:", net_pairs, "of", len(pairs))
for ex in examples:
    print(ex)
