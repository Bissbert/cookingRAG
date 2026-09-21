#!/usr/bin/env python3
"""Summarise a recipeExport-*.json file produced by ingest_recipes.py.

The repository ships one such export, committed by the author after a real
ingest run. This script reports what is in it, and checks each record against
the Recipe model as it exists in util/recipe.py today.

    python3 tools/inspect_export.py [export.json]

Only the standard library is required for the summary. The schema check is
skipped automatically when pydantic and util.recipe are not importable.
"""

import glob
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def summarise(records):
    keys = sorted({k for r in records for k in r})
    print("Records: %d" % len(records))
    print("Keys present across all records: %s" % ", ".join("`%s`" % k for k in keys))
    print()
    print("| # | title | ingredients | instruction steps | cook_time | type | dietary_preference |")
    print("| ---: | --- | ---: | ---: | --- | --- | --- |")
    for i, r in enumerate(records, 1):
        ing = r.get("ingredients") or []
        ins = r.get("instructions") or []
        print("| %d | %s | %d | %d | %s | %s | %s |"
              % (i, r.get("title", ""), len(ing), len(ins),
                 r.get("cook_time") or "(empty)",
                 r.get("type", ""), r.get("dietary_preference", "")))
    print()
    titles = [r.get("title", "") for r in records]
    for t in sorted(set(titles)):
        print("title %-40s appears %d time(s)" % ("%r" % t, titles.count(t)))


def schema_check(records):
    sys.path.insert(0, REPO)
    try:
        from pydantic import ValidationError
        from util.recipe import Recipe
    except Exception as exc:  # noqa: BLE001
        print()
        print("Schema check skipped: %s: %s" % (type(exc).__name__, exc))
        return
    print()
    print("Validated against util/recipe.py Recipe:")
    for i, r in enumerate(records, 1):
        try:
            Recipe(**r)
            print("  record %d: validates" % i)
        except ValidationError as exc:
            detail = "; ".join(
                "%s: %s" % (".".join(map(str, e["loc"])), e["msg"])
                for e in exc.errors()
            )
            print("  record %d: FAILS - %s" % (i, detail))


def main():
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = sorted(glob.glob(os.path.join(REPO, "recipeExport-*.json")))
    if not paths:
        print("no recipeExport-*.json found", file=sys.stderr)
        return 1
    for path in paths:
        print("== %s" % os.path.basename(path))
        records = load(path)
        summarise(records)
        schema_check(records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
