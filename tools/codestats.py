#!/usr/bin/env python3
"""Count lines and bytes of every Python file in the repository.

Produces the source-size table in README.md and docs/README.md.

    python3 tools/codestats.py
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    "ingest_recipes.py",
    "query_recipes.py",
    "util/recipe.py",
    "util/json_util.py",
    "util/embedding_util.py",
    "util/database_conection.py",
    "util/ingestion_model_interaction.py",
]


def stats(relpath):
    path = os.path.join(REPO, relpath)
    with open(path, "rb") as fh:
        blob = fh.read()
    return blob.count(b"\n"), len(blob)


def main():
    rows = []
    for relpath in FILES:
        if not os.path.exists(os.path.join(REPO, relpath)):
            print("missing: %s" % relpath, file=sys.stderr)
            continue
        lines, byts = stats(relpath)
        rows.append((relpath, lines, byts))

    width = max(len(r[0]) for r in rows) + 2
    print("| %-*s | Lines | Bytes |" % (width, "File"))
    print("| %s | -----: | ----: |" % ("-" * width))
    for relpath, lines, byts in rows:
        print("| %-*s | %5d | %6s |"
              % (width, "`%s`" % relpath, lines, format(byts, ",")))
    print("| %-*s | %5s | %6s |"
          % (width, "**total**",
             "**%d**" % sum(r[1] for r in rows),
             "**%s**" % format(sum(r[2] for r in rows), ",")))


if __name__ == "__main__":
    main()
