# SSW 625 Project: Hidden Divergence in Reused Agent Skills

Scripts that measure how often copied agent skills contain hidden divergence, using the GitSkills sample dataset (13,000 distinct skill contents).

## Requirements

- Python 3.11
- `pip install datasketch`
- `agent_skills_sample.db` from the GitSkills sample repo

## Setup

Place `agent_skills_sample.db` in the same folder as the scripts. Nothing else to configure.

## How to run

Run the scripts in order. Each one feeds the next.

1. `python 01_inspect.py` — verifies the database. Prints table names, total row counts, and the 13,000 distinct contents check.
2. `python 02_prevalence.py` — ranks distinct skills by copy count. Prints the top 20 most copied skills and the concentration buckets.
3. `python 03_near_dupe.py` — finds near duplicate skills with MinHash and LSH at 0.8 Jaccard threshold. Prints candidate pairs, verified near duplicate pairs, and distinct contents involved. Takes about ten minutes.
4. `python 04_divergence.py` — diffs each near duplicate pair for newly added command execution and network access. Prints pair counts and examples. Needs `pairs.csv` from script 3.
5. `python 05_exec_bundling.py` — counts distinct skills that bundle scripts and their copy counts.

## What the numbers mean

The printed numbers feed the Experiments section of the report: prevalence of reuse, near duplicates missed by exact hashing, and divergence toward risky capabilities.

## Repo layout

agent_skills_sample.db
01_inspect.py
02_prevalence.py
03_near_dupe.py
04_divergence.py
05_exec_bundling.py
pairs.csv
README.md