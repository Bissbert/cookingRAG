#!/bin/sh
# Run every measurement in docs/measurement.md inside Linux containers.
#
#   sh tools/linux-run.sh > media/captures/linux-run.txt
#
# Starts a throwaway pgvector server and a python:3.12 container on a private
# Docker network, installs requirements.txt, and runs each tool in tools/
# against a copy of the repository. The repository itself is mounted
# read-only. No Ollama models are available in the containers, so nothing
# here runs a vision, structuring or embedding model. Everything is removed
# on exit.

set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
NET=cookingrag-run-$$
DB=cookingrag-db-$$

cleanup() {
    docker rm -f "$DB" >/dev/null 2>&1 || true
    docker network rm "$NET" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

docker pull -q pgvector/pgvector:pg16 >/dev/null
docker pull -q python:3.12-slim-bookworm >/dev/null
docker network create "$NET" >/dev/null
docker run -d --name "$DB" --network "$NET" \
    -e POSTGRES_PASSWORD=measure pgvector/pgvector:pg16 >/dev/null

docker run --rm --network "$NET" -v "$REPO":/repo:ro \
    -e PG_HOST="$DB" -e PG_PASSWORD=measure \
    python:3.12-slim-bookworm sh -c '
set -u
section() { printf "\n=== %s\n" "$*"; }

apt-get -qq update >/dev/null 2>&1 && apt-get -qq install -y git fonts-dejavu-core >/dev/null 2>&1
cp -r /repo /tmp/cr && cd /tmp/cr

section "environment"
uname -srm
python3 --version
pip --version | cut -d" " -f1-2

section "pip install -r requirements.txt"
pip install -q --disable-pip-version-check --root-user-action=ignore \
    -r requirements.txt Pillow >/tmp/pip.log 2>&1
echo "exit=$?"
pip show pydantic llama-index-core 2>/dev/null | grep -E "^(Name|Version)"

for i in $(seq 30); do
    python3 -c "import psycopg2,os; psycopg2.connect(host=os.environ[\"PG_HOST\"], user=\"postgres\", password=\"measure\").close()" 2>/dev/null && break
    sleep 1
done

section "tools/envcheck.py"
python3 tools/envcheck.py

section "tools/codestats.py"
python3 tools/codestats.py

section "entry points: --help"
python3 ingest_recipes.py --help >/dev/null 2>&1; echo "ingest_recipes.py --help  exit=$?"
python3 query_recipes.py --help >/dev/null 2>&1;  echo "query_recipes.py --help   exit=$?"

section "tools/show_schema.py"
python3 tools/show_schema.py

section "tools/node_preview.py"
python3 tools/node_preview.py

section "tools/inspect_export.py"
python3 tools/inspect_export.py

section "tools/repo_size.py"
python3 tools/repo_size.py

section "setup_database() twice, with a database name that needs quoting"
PG_DB_NAME="recipe-db; x" python3 -c "
from util.database_conection import setup_database
setup_database(); setup_database()"
echo "exit=$?"

section "query_recipes.py against an empty store, no OpenAI key"
PG_DB_NAME="recipe-db; x" python3 query_recipes.py something vegetarian with lentils >/tmp/q.log 2>&1
echo "exit=$?"
grep -E "^(ValueError|Could not load|No API key)" /tmp/q.log

section "tools/make_media.py reproduces media/corpus.jpg"
python3 tools/make_media.py >/dev/null
python3 -c "
from PIL import Image, ImageChops
import PIL
a = Image.open(\"media/corpus.jpg\"); b = Image.open(\"/repo/media/corpus.jpg\")
print(\"Pillow\", PIL.__version__, \"size\", a.size, \"committed\", b.size)
d = ImageChops.difference(a.convert(\"RGB\"), b.convert(\"RGB\"))
print(\"max per-channel pixel difference:\", max(x[1] for x in d.getextrema()))
"
cmp -s media/corpus.jpg /repo/media/corpus.jpg && echo "byte-identical" || echo "not byte-identical"
'
