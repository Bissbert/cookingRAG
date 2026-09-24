# How this was measured

[← back to the overview](../README.md)

Every number in this repository's documentation comes from a command that was
run in Linux containers, not on the author's workstation. One script,
[`tools/linux-run.sh`](../tools/linux-run.sh), does all of it:

```sh
sh tools/linux-run.sh > media/captures/linux-run.txt
```

It starts a throwaway `pgvector/pgvector:pg16` server and a
`python:3.12-slim-bookworm` container on a private Docker network, installs
`requirements.txt`, and runs each script in [`tools/`](../tools) against a copy
of the repository (the checkout itself is mounted read-only). Its full output is
[`media/captures/linux-run.txt`](../media/captures/linux-run.txt); every block
quoted below is taken from that file.

**No model runs anywhere on this page.** The containers have no Ollama daemon
and none of the three models the code names, so nothing here reports an ingest
time, a query latency, a recall figure or a similarity score. What is reported
is what runs without models: dependency resolution, the entry points, the
database setup, the generated schema, the node text, and an analysis of the one
export file the author committed after their own run.

## What is available in the containers

`tools/envcheck.py` probes all three moving parts:

```
| Component                   | Status |
| --------------------------- | --- |
| python                      | OK   3.12.14 |
| ollama daemon               | FAIL unreachable at http://localhost:11434 |
|   model llama3.2-vision:90b | FAIL unknown - daemon down (util/ingestion_model_interaction.py:14) |
|   model qwq                 | FAIL unknown - daemon down (util/ingestion_model_interaction.py:17) |
|   model bge-m3              | FAIL unknown - daemon down (util/embedding_util.py:10) |
| postgres tcp                | OK   cookingrag-db-49291:5432 open |
| psycopg2                    | OK   importable |
| llama_index.core            | OK   0.12.2 |
```

PostgreSQL with pgvector is there; the models are not. `llama3.2-vision:90b`
alone is a ~55 GB download, which is why the run stops short of the models.

## Source sizes

`tools/codestats.py` reads each file and counts newlines and bytes.

| File | Lines | Bytes |
| --- | ---: | ---: |
| `ingest_recipes.py` | 127 | 3,863 |
| `query_recipes.py` | 53 | 1,740 |
| `util/recipe.py` | 32 | 1,498 |
| `util/json_util.py` | 15 | 411 |
| `util/embedding_util.py` | 51 | 1,671 |
| `util/database_conection.py` | 66 | 2,349 |
| `util/ingestion_model_interaction.py` | 164 | 5,718 |
| **total** | **508** | **17,250** |

## Dependency resolution

`pip install -r requirements.txt` exits 0 on Python 3.12.14 with pip 25.0.1,
and installs **pydantic 2.9.2** and **llama-index-core 0.12.2**. The earlier
`pydantic==1.10.17` pin that made the file unresolvable was replaced in
`8b10cf36` (BUG-05).

## The two entry points

| Command | Result |
|---|---|
| `python ingest_recipes.py --help` | exit 0 |
| `python query_recipes.py --help` | exit 0 |

Both import cleanly against the pinned `llama_index` 0.12.2.

## Database setup

`setup_database()` from `util/database_conection.py`, called twice against the
pgvector server with a database name that needs quoting
(`PG_DB_NAME="recipe-db; x"`):

```
Database 'recipe-db; x' created.
Database 'recipe-db; x' already exists.
exit=0
```

The name is passed as a quoted identifier, not pasted into the SQL, and the
second call sees the database the first one made. See
[04 — Storage](04-storage.md).

## A query with no models

`query_recipes.py something vegetarian with lentils` against that database,
with no `OPENAI_API_KEY` set:

```
exit=1
ValueError: No API key found for OpenAI.
Could not load OpenAI embedding model. If you intended to use OpenAI, please check your OPENAI_API_KEY.
```

The script imports and connects, then stops because it configures no local
model and llama_index falls back to OpenAI. That is BUG-04, still open. See
[05 — Query](05-query.md).

## The generated database schema

`tools/show_schema.py` calls the same `get_data_model()` factory that
`PGVectorStore` uses internally, with the arguments `util/database_conection.py`
passes, and compiles the result for PostgreSQL:

```sql
CREATE TABLE public.data_recipes (
	id BIGSERIAL NOT NULL,
	text VARCHAR NOT NULL,
	metadata_ JSON,
	node_id VARCHAR,
	embedding VECTOR(1536),
	PRIMARY KEY (id)
)
```

No HNSW or IVFFlat index is created, so similarity search is a sequential scan.
The `VECTOR(1536)` width is BUG-09, still open; see
[04 — Storage](04-storage.md).

## What `get_nodes_from_objs()` emits

`tools/node_preview.py` builds one fully populated `Recipe`, passes it through
`util/embedding_util.py`, and prints the node text:

```
Title: Pariser Zwiebelsuppe

Cook Time: 45 minutes
Ingredients:
- 375 g Zwiebeln
- 50 g Butter
- 40 g Mehl
- 1 l Bruehe

Instructions:
1. Zwiebeln in feine Scheiben hobeln. 2. In Butter glasig duensten. 3. Mehl aufstreuen und aufkochen lassen.
```

```
Ingredient names reached the node text: True
Instruction text reached the node text: True
Characters in: 172   Characters out: 244
```

The two booleans come from a substring search against the node text. See
[03 — Indexing](03-indexing.md).

## The committed export

`recipeExport-3889e5c2-fd85-4e50-8a61-024a12744127.json` was committed by the
author in `e9eb1a43` and is the only surviving artifact of a real run. It is
evidence about *that* run, on an unknown model build at an unknown date, not a
benchmark. `tools/inspect_export.py` summarises it:

| # | title | ingredients | instruction steps | cook_time | type | dietary_preference |
| ---: | --- | ---: | ---: | --- | --- | --- |
| 1 | Mehlsuppe mit Brötchen und Eier | 10 | 9 | 20-30 minutes | baking | vegetarian |
| 2 | Spaetzle im Brei | 5 | 5 | 20 minutes | baking | vegetarian |
| 3 | Spaetzle im Brei | 4 | 5 | (empty) | baking | vegetarian |
| 4 | Spaetzle im Brei | 1 | 1 | 30 minutes | cooking | vegetarian |
| 5 | Spaetzle im Brei | 4 | 7 | 15-20 minutes | cooking | vegetarian |

Five records for the five images in `testRecipes/`. Every record carries
`title`, `ingredients`, `instructions`, `cook_time`, `type` and
`dietary_preference`, and none carries `instructionsAsString`, so all five fail
validation against `util/recipe.py`. The export predates the field rename.

Comparing those titles against the images themselves (they are legible in
[`media/corpus.jpg`](../media/corpus.jpg)) is a manual, visual check, reported
as such in [02 — Extraction](02-extraction.md). No scoring metric was computed.

## Repository size

`tools/repo_size.py` walks the whole object graph and attributes every blob to a
top-level path:

| Top-level path | Blobs | Uncompressed bytes | Share |
| --- | ---: | ---: | ---: |
| `venv` | 14,948 | 253,436,221 | 99.2 % |
| `testRecipes` | 5 | 1,548,272 | 0.6 % |
| `docs` | 18 | 143,440 | 0.1 % |
| everything else | 52 | 335,645 | 0.1 % |
| **total** | **15,023** | **255,463,578** | |

`git count-objects -vH` reports `in-pack: 16965`, `size-pack: 78.31 MiB`. A
virtualenv was committed in the initial commit `d3ea1ea4` and deleted in
`7e9c095f`; deleting it removed it from the working tree but not from history.

## The contact sheet

`media/corpus.jpg` is built by `tools/make_media.py` from the five JPEGs in
`testRecipes/`, downscaled to 260 px wide and laid out in filename order, with
captions in DejaVu Sans. It was rendered in the Python container, and a re-run
there is byte-identical to the committed file. It reproduces committed
repository content; it is not a capture of a program run.

## Environment

| | |
|---|---|
| Host kernel | Linux 6.5.11-linuxkit, aarch64 (Docker Desktop VM) |
| Python container | `python:3.12-slim-bookworm` (`sha256:392307d2…23564e`), Python 3.12.14, pip 25.0.1, Pillow 12.3.0 |
| Database container | `pgvector/pgvector:pg16` (`sha256:ccc6e83d…fb4d6b`) |
| Ollama | none |
| Date | 2026-09-24 |

## Things deliberately not measured

| Quantity | Why not |
|---|---|
| Ingest wall-clock time per image | Vision model not available. |
| Query latency | No embedding model. |
| Retrieval quality / recall | Would need a labelled query set; none exists. |
| Extraction accuracy as a score | n = 5, one run, unknown model build. Described qualitatively instead. |
| Actual `bge-m3` embedding width | Model not pulled. The mismatch with `embed_dim=1536` is discussed in [04 — Storage](04-storage.md) as a code-level observation. |
