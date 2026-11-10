import sqlite3
import re 
from datasketch import MinHash
from datasketch import MinHashLSH
import csv

conn = sqlite3.connect("agent_skills_sample.db")
rows = conn.execute("""
    SELECT file_sha, content FROM artifacts
    WHERE content_fetched = 1 AND content IS NOT NULL
""").fetchall()
print("loaded:", len(rows))


def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def shingles(text, k=5):
    words = text.split()
    return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

doc = normalize(rows[0][1])
print("shingles in first doc:", len(shingles(doc)))

signatures = {}
for i, (sha, content) in enumerate(rows):
    m = MinHash(num_perm=128)
    for s in shingles(normalize(content)):
        m.update(s.encode("utf-8"))
    signatures[i] = m
    if (i + 1) % 2000 == 0:
        print("signed", i + 1)

print("done, total signatures:", len(signatures))

lsh = MinHashLSH(threshold=0.8, num_perm=128)
for i, sig in signatures.items():
    lsh.insert(i, sig)

pairs = set()
for i, sig in signatures.items():
    for j in lsh.query(sig):
        if j > i:
            pairs.add((i, j))
    if (i + 1) % 2000 == 0:
        print("queried", i + 1)

print("candidate pairs:", len(pairs))

def jaccard(a, b):
    union = len(a | b)
    if union == 0:
        return 0.0
    return len(a & b) / union


shingle_cache = {}
def get_shingles(i):
    if i not in shingle_cache:
        shingle_cache[i] = shingles(normalize(rows[i][1]))
    return shingle_cache[i]

kept = []
for i, j in pairs:
    if rows[i][0] == rows[j][0]:
        continue
    score = jaccard(get_shingles(i), get_shingles(j))
    if score >= 0.8:
        kept.append((i, j, score))

print("near duplicate pairs:", len(kept))
involved = {i for i, j, s in kept} | {j for i, j, s in kept}
print("distinct contents involved:", len(involved))




with open("pairs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["i", "j", "score"])
    for i, j, s in kept:
        w.writerow([i, j, s])
print("saved pairs.csv")
