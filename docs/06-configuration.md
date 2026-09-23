# 6 — Configuration

[← back to the overview](../README.md)

Everything configurable in cookingRAG is an environment variable read at import
time, plus four values that are hard-coded and require a source edit.

## Environment variables

All five are read in **two** places —
[`util/database_conection.py`](../util/database_conection.py) lines 7–11 and
[`query_recipes.py`](../query_recipes.py) lines 11–15 — as independent copies
with identical defaults.

| Variable | Default | Used for | If unset |
|---|---|---|---|
| `PG_HOST` | `localhost` | PostgreSQL host | Fine for a local server. |
| `PG_PORT` | `5432` | PostgreSQL port | Fine for a default install. |
| `PG_USER` | `postgres` | PostgreSQL role | Must be able to `CREATEDB`; `setup_database()` issues `CREATE DATABASE`. |
| `PG_PASSWORD` | `your_database_password` | PostgreSQL password | **Breaks.** The literal default is used and PostgreSQL rejects it: `FATAL: password authentication failed`. There is no check for a missing value. |
| `PG_DB_NAME` | `recipe_db` | Database to create and use | Fine. Note it is interpolated unquoted into `CREATE DATABASE {db_name}`, so names needing quoting fail. |

```mermaid
flowchart LR
    ENV["environment"] --> DC["util/database_conection.py<br/><i>module import</i>"]
    ENV --> QR["query_recipes.py<br/><i>module import</i>"]
    DC --> CS["connection_string<br/>→ database <b>postgres</b>"]
    DC --> VS1["PGVectorStore<br/>→ database <b>PG_DB_NAME</b>"]
    QR --> VS2["PGVectorStore<br/><i>duplicate copy</i>"]

    style ENV fill:#1f6feb,stroke:#58a6ff,color:#fff
    style QR fill:#da3633,stroke:#f85149,color:#fff
```

Because the reads happen at module scope, `os.environ[...] = ...` after import
has no effect. Export before launching the process.

## Not configurable without editing source

| Value | Set in | Line |
|---|---|---|
| Ollama base URL `http://localhost:11434` | `util/embedding_util.py` | 11 |
| Vision model `llama3.2-vision:90b` | `util/ingestion_model_interaction.py` | 14 |
| Structuring model `qwq` | `util/ingestion_model_interaction.py` | 17 |
| Embedding model `bge-m3` | `util/embedding_util.py` | 10 |
| Table name `recipes` → `data_recipes` | `util/database_conection.py` | 58 |
| `embed_dim=1536` | `util/database_conection.py` | 59 |
| Request timeout `600.0` s (both models) | `util/ingestion_model_interaction.py` | 14, 17 |
| Retries `3`, delay `5` s | `util/ingestion_model_interaction.py` | 53 |
| Images sampled per run `10` | `ingest_recipes.py` | 23 |
| `similarity_top_k=5` | `query_recipes.py` | 33 |

`OLLAMA_HOST` is **not** honoured — the base URL is passed explicitly to
`OllamaEmbedding`, and the two `Ollama`/`OllamaMultiModal` constructors take no
`base_url` at all, so they use the library default of `http://localhost:11434`.
A remote Ollama needs source edits in two files.

## Required models

Three, all of which must be present on the Ollama daemon before ingestion:

| Model | Role | Declared in |
|---|---|---|
| `llama3.2-vision:90b` | image → free-text recipe | `util/ingestion_model_interaction.py:14` |
| `qwq` | free text → structured `Recipe` | `util/ingestion_model_interaction.py:17` |
| `bge-m3` | text → embedding vector | `util/embedding_util.py:10` |

```sh
ollama pull llama3.2-vision:90b
ollama pull qwq
ollama pull bge-m3
```

`llama3.2-vision:90b` is the 90-billion-parameter variant; the download is on
the order of 55 GB and it needs a correspondingly large amount of memory to
serve. `llama3.2-vision:11b` is the smaller sibling, and switching to it is a
one-line edit — but no measurement in this repository says anything about the
quality difference, so that is a substitution to make and then evaluate, not a
recommendation.

## Checking a machine

`tools/envcheck.py` tests all of the above and prints a table:

```sh
python3 tools/envcheck.py
```

It exits 0 only when the daemon is up, all three models are present, and the
PostgreSQL port accepts a connection. It uses the standard library only, so it
runs before the project's dependencies are installed — though it will report
`psycopg2` and `llama_index.core` as missing until they are.

## PostgreSQL requirements

| Requirement | Why |
|---|---|
| Server reachable on `PG_HOST:PG_PORT` | Both connections. |
| Role with `CREATEDB` | `setup_database()` may issue `CREATE DATABASE`. |
| `pgvector` available to install | `PGVectorStore` issues `CREATE EXTENSION IF NOT EXISTS vector`, which needs the extension files present on the server and a role permitted to create extensions (superuser on most installs). |

The `CREATE EXTENSION` is the requirement most easily missed: a stock PostgreSQL
package does not include pgvector. The `pgvector/pgvector` container images ship
it, as do the `postgresql-NN-pgvector` packages on Debian and Ubuntu.

## Back

[← overview](../README.md) · [docs index](README.md)
