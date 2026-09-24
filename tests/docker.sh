#!/bin/sh
# Run the test suite inside Linux containers.
#
#   sh tests/docker.sh
#
# Starts a throwaway pgvector server and a python:3.12 container on a private
# Docker network, installs requirements.txt and pytest, and runs pytest on a
# copy of the repository. The repository is mounted read-only. No Ollama
# daemon and no OpenAI key are available; the tests fake the Ollama models.
# Everything is removed on exit. Extra arguments are passed to pytest.

set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
NET=cookingrag-test-$$
DB=cookingrag-testdb-$$

cleanup() {
    docker rm -f "$DB" >/dev/null 2>&1 || true
    docker network rm "$NET" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

docker pull -q pgvector/pgvector:pg16 >/dev/null
docker pull -q python:3.12-slim-bookworm >/dev/null
docker network create "$NET" >/dev/null
docker run -d --name "$DB" --network "$NET" \
    -e POSTGRES_PASSWORD=test pgvector/pgvector:pg16 >/dev/null

docker run --rm --network "$NET" -v "$REPO":/repo:ro \
    -e PG_HOST="$DB" -e PG_PASSWORD=test \
    python:3.12-slim-bookworm sh -c '
set -e
cp -r /repo /tmp/cr && cd /tmp/cr
pip install -q --disable-pip-version-check --root-user-action=ignore \
    -r requirements.txt pytest >/tmp/pip.log 2>&1 || { cat /tmp/pip.log; exit 1; }
for i in $(seq 30); do
    python3 -c "import psycopg2,os; psycopg2.connect(host=os.environ[\"PG_HOST\"], user=\"postgres\", password=\"test\").close()" 2>/dev/null && break
    sleep 1
done
python3 -m pytest -p no:cacheprovider -q tests "$@"
' sh "$@"
