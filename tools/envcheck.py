#!/usr/bin/env python3
"""Report which parts of the cookingRAG stack are reachable from this machine.

cookingRAG needs three things to run end to end: a Python environment with the
pinned libraries, an Ollama daemon holding three specific models, and a
PostgreSQL server with the pgvector extension. This script checks all three and
prints a table, so the reason a run did or did not happen is recorded rather
than assumed.

    python3 tools/envcheck.py

Exit status is 0 when everything needed for a full run is present, 1 otherwise.
Only the standard library is used, so it runs outside the project venv too.
"""

import json
import os
import socket
import sys
import urllib.error
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
if not OLLAMA_URL.startswith("http"):
    OLLAMA_URL = "http://" + OLLAMA_URL

PG_HOST = os.environ.get("PG_HOST", "localhost")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))

# Model names as hard-coded in the source, with the file that pins each one.
REQUIRED_MODELS = [
    ("llama3.2-vision:90b", "util/ingestion_model_interaction.py:23"),
    ("qwq", "util/ingestion_model_interaction.py:26"),
    ("bge-m3", "util/embedding_util.py:12"),
]


def ollama_models():
    try:
        with urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=5) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return None, str(exc)
    return [m.get("name", "") for m in data.get("models", [])], None


def model_present(name, available):
    """Ollama treats a bare name as ':latest'; compare both spellings."""
    wanted = name if ":" in name else name + ":latest"
    return wanted in available or name in available


def tcp_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except OSError:
        return False


def main():
    rows = []

    rows.append(("python", "%d.%d.%d" % sys.version_info[:3], True))

    available, err = ollama_models()
    if available is None:
        rows.append(("ollama daemon", "unreachable at %s (%s)" % (OLLAMA_URL, err), False))
        for name, where in REQUIRED_MODELS:
            rows.append(("  model %s" % name, "unknown - daemon down (%s)" % where, False))
    else:
        rows.append(("ollama daemon", "up at %s, %d model(s)" % (OLLAMA_URL, len(available)), True))
        for name, where in REQUIRED_MODELS:
            ok = model_present(name, available)
            rows.append(("  model %s" % name,
                         "present" if ok else "ABSENT - ollama pull %s (%s)" % (name, where),
                         ok))

    pg_up = tcp_open(PG_HOST, PG_PORT)
    rows.append(("postgres tcp", "%s:%d %s" % (PG_HOST, PG_PORT, "open" if pg_up else "closed"), pg_up))

    try:
        import psycopg2  # noqa: F401
        rows.append(("psycopg2", "importable", True))
    except ImportError:
        rows.append(("psycopg2", "not installed", False))

    try:
        import llama_index.core  # noqa: F401
        from llama_index.core import __version__ as liv
        rows.append(("llama_index.core", liv, True))
    except Exception as exc:  # noqa: BLE001
        rows.append(("llama_index.core", "not importable (%s)" % type(exc).__name__, False))

    width = max(len(r[0]) for r in rows)
    print("| %-*s | Status |" % (width, "Component"))
    print("| %s | --- |" % ("-" * width))
    for name, detail, ok in rows:
        print("| %-*s | %s %s |" % (width, name, "OK  " if ok else "FAIL", detail))

    missing = [r[0].strip() for r in rows if not r[2]]
    print()
    if missing:
        print("Cannot run end to end. Missing: %s" % ", ".join(missing))
        return 1
    print("All components present; a full ingest + query run is possible.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
