#!/usr/bin/env python3
"""Explain the on-disk size of this repository.

The working tree holds 17 files and well under 2 MB of content, but a fresh
clone transfers far more. This script attributes every blob in the full object
graph to a top-level path so the difference is visible.

    python3 tools/repo_size.py
"""

import collections
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*args):
    return subprocess.run(
        ["git", "-C", REPO] + list(args),
        capture_output=True, text=True, check=True,
    ).stdout


def main():
    try:
        listing = git("rev-list", "--objects", "--all")
    except subprocess.CalledProcessError as exc:
        print("git failed: %s" % exc, file=sys.stderr)
        return 1

    check = subprocess.run(
        ["git", "-C", REPO, "cat-file",
         "--batch-check=%(objecttype) %(objectname) %(objectsize) %(rest)"],
        input=listing, capture_output=True, text=True, check=True,
    ).stdout

    by_top = collections.Counter()
    count_top = collections.Counter()
    total_objects = 0

    for line in check.splitlines():
        parts = line.split(maxsplit=3)
        if len(parts) < 3 or parts[0] != "blob":
            continue
        total_objects += 1
        size = int(parts[2])
        path = parts[3] if len(parts) > 3 else "(no path)"
        top = path.split("/")[0] if "/" in path else path
        by_top[top] += size
        count_top[top] += 1

    grand = sum(by_top.values())

    print("Blobs in the full object graph (all refs, all history)")
    print()
    print("| Top-level path | Blobs | Uncompressed bytes | Share |")
    print("| --- | ---: | ---: | ---: |")
    for top, size in by_top.most_common(12):
        print("| `%s` | %s | %s | %.1f %% |"
              % (top, format(count_top[top], ","), format(size, ","),
                 100.0 * size / grand if grand else 0.0))
    print("| **total** | **%s** | **%s** | |"
          % (format(total_objects, ","), format(grand, ",")))
    print()

    print("Packed size reported by git:")
    print()
    for line in git("count-objects", "-vH").splitlines():
        if line.startswith(("size-pack", "in-pack", "count:")):
            print("    %s" % line)
    print()

    commits = git("log", "--all", "--oneline", "--", "venv").splitlines()
    if commits:
        print("Commits touching `venv/`:")
        for line in commits:
            print("    %s" % line)


if __name__ == "__main__":
    sys.exit(main() or 0)
