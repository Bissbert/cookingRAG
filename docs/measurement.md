# How this was measured

[← back to the overview](../README.md)

Every number in this repository's documentation comes from a command that was
actually run on one machine. The scripts that produced them live in
[`tools/`](../tools) and are plain Python 3. Only `tools/make_media.py` needs a
non-stdlib package (Pillow); the others need either nothing or the project's own
dependencies.

**The pipeline itself was never run during this documentation pass.** Nothing in
these docs reports an ingest time, a query latency, a recall figure or a
similarity score, because no ingest and no query happened. What is reported
instead is static: source sizes, dependency resolution, import behaviour, the
generated SQL schema, and an analysis of the one export file the author
committed after their own run. The next section says exactly why the pipeline
could not be run.

## What could not be run, and why

`tools/envcheck.py` probes all three moving parts and prints a table. Run on
2026-09-21 with the project's dependencies importable:

```
| Component                   | Status |
| --------------------------- | --- |
| python                      | OK   3.11.5 |
| ollama daemon               | OK   up at http://localhost:11434, 5 model(s) |
|   model llama3.2-vision:90b | FAIL ABSENT - ollama pull llama3.2-vision:90b |
|   model qwq                 | FAIL ABSENT - ollama pull qwq |
|   model bge-m3              | FAIL ABSENT - ollama pull bge-m3 |
| postgres tcp                | FAIL localhost:5432 closed |
| psycopg2                    | OK   importable |
| llama_index.core            | OK   0.12.2 |
```

Two independent blockers, either of which alone is enough:

| Blocker | Detail |
|---|---|
| Models absent | The Ollama daemon is running but holds none of the three models the code names. `llama3.2-vision:90b` alone is a ~55 GB download. |
| No PostgreSQL | Nothing listens on `localhost:5432`; no `psql` binary is installed and the local Docker daemon is not running, so no pgvector instance could be brought up either. |

Per the rule this pass works under: **diagrams only, no invented output.** There
are no GIFs of a run in `media/`, no timing tables, and no retrieval-quality
numbers anywhere in these docs.

## Source sizes

`tools/codestats.py` reads each file and counts newlines and bytes.

```sh
python3 tools/codestats.py
```

| File | Lines | Bytes |
| --- | ---: | ---: |
| `ingest_recipes.py` | 126 | 3,843 |
| `query_recipes.py` | 51 | 1,683 |
| `util/recipe.py` | 31 | 1,567 |
| `util/json_util.py` | 15 | 411 |
| `util/embedding_util.py` | 55 | 1,842 |
| `util/database_conection.py` | 62 | 2,254 |
| `util/ingestion_model_interaction.py` | 140 | 5,100 |
| **total** | **480** | **16,700** |

## Dependency resolution

`requirements.txt` was resolved in a throwaway virtualenv on Python 3.11.5 with
pip 26.2.1:

```sh
python3 -m venv /tmp/v && /tmp/v/bin/pip install --dry-run -r requirements.txt
```

It fails, and the failure is not environmental:

```
ERROR: Cannot install -r requirements.txt (line 8) and pydantic==1.10.17
because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested pydantic==1.10.17
    llama-index-core 0.12.2 depends on pydantic<2.10.0 and >=2.7.0

ERROR: ResolutionImpossible
```

Dropping only the `pydantic==1.10.17` line makes the same file install cleanly
(exit 0), and pip then selects **pydantic 2.9.2**. Every other check on this
page was run inside that environment.

## Import behaviour of the two entry points

With those dependencies installed, from the repository root:

| Command | Result |
|---|---|
| `python ingest_recipes.py --help` | exits 0, prints usage |
| `python query_recipes.py --help` | **`ImportError`**, never reaches `argparse` |

Both of `query_recipes.py`'s imports fail against the pinned `llama_index`
0.12.2:

```
from llama_index import StorageContext, VectorStoreIndex
  ImportError: cannot import name 'StorageContext' from 'llama_index'
from llama_index.vector_stores import PGVectorStore
  ImportError: cannot import name 'PGVectorStore' from 'llama_index.vector_stores'
```

All five `util/` modules import cleanly, so the failure is confined to
`query_recipes.py`. See [05 — Query](05-query.md).

## The generated database schema

No database was contacted. `tools/show_schema.py` calls the same
`get_data_model()` factory that `PGVectorStore` uses internally, with the exact
arguments `util/database_conection.py` passes, and compiles the result for the
PostgreSQL dialect:

```sh
python3 tools/show_schema.py
```

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

This is how the table name `data_recipes` and the absence of a vector index were
established, rather than by reading the call site. See
[04 — Storage](04-storage.md).

## What `get_nodes_from_objs()` emits

`tools/node_preview.py` constructs one fully populated `Recipe` using the model
in `util/recipe.py`, passes it through `util/embedding_util.py`, and prints the
node text verbatim:

```sh
python3 tools/node_preview.py
```

Input: title, 4 ingredients, a 3-step instruction string. Output:

```
Title: Pariser Zwiebelsuppe

Cook Time: 45 minutes
Ingredients:
- :
- :
- :
- :

Instructions:
```

```
Ingredient names reached the node text: False
Instruction text reached the node text: False
Characters in: 172   Characters out: 99
```

The script reports the two booleans by substring search against the node text,
not by inspection. See [03 — Indexing](03-indexing.md) for the cause.

## The committed export

`recipeExport-3889e5c2-fd85-4e50-8a61-024a12744127.json` was committed by the
author in `e9eb1a43` and is the only surviving artifact of a real run. It is
evidence about *that* run, on an unknown model build at an unknown date — not a
benchmark. `tools/inspect_export.py` summarises it:

```sh
python3 tools/inspect_export.py
```

| # | title | ingredients | instruction steps | cook_time | type | dietary_preference |
| ---: | --- | ---: | ---: | --- | --- | --- |
| 1 | Mehlsuppe mit Brötchen und Eier | 10 | 9 | 20-30 minutes | baking | vegetarian |
| 2 | Spaetzle im Brei | 5 | 5 | 20 minutes | baking | vegetarian |
| 3 | Spaetzle im Brei | 4 | 5 | (empty) | baking | vegetarian |
| 4 | Spaetzle im Brei | 1 | 1 | 30 minutes | cooking | vegetarian |
| 5 | Spaetzle im Brei | 4 | 7 | 15-20 minutes | cooking | vegetarian |

Five records for the five images in `testRecipes/`. Every record carries the
keys
`title`, `ingredients`, `instructions`, `cook_time`, `type`,
`dietary_preference` — and **none** carries `instructionsAsString`, so all five
fail validation against `util/recipe.py` as it stands today. The export predates
the field rename.

Comparing those titles against the images themselves (they are legible in
[`media/corpus.jpg`](../media/corpus.jpg)) is a manual, visual check, and it is
reported as such in [02 — Extraction](02-extraction.md). No scoring metric was
computed.

## Repository size

`tools/repo_size.py` walks the whole object graph and attributes every blob to a
top-level path:

```sh
python3 tools/repo_size.py
```

| Top-level path | Blobs | Uncompressed bytes | Share |
| --- | ---: | ---: | ---: |
| `venv` | 14,948 | 253,436,221 | 99.3 % |
| `testRecipes` | 5 | 1,548,272 | 0.6 % |
| `README.md` | 7 | 74,690 | 0.0 % |
| `util` | 13 | 24,569 | 0.0 % |
| everything else | 11 | 30,065 | 0.0 % |
| **total** | **14,984** | **255,113,817** | |

`git count-objects -vH` reports `in-pack: 16885`, `size-pack: 78.14 MiB`. A
virtualenv was committed in the initial commit `d3ea1ea4` and deleted in
`7e9c095f`; deleting it removed it from the working tree but not from history.
See the note in the main README.

## The contact sheet

`media/corpus.jpg` is built by `tools/make_media.py` from the five JPEGs in
`testRecipes/`, downscaled to 260 px wide and laid out in filename order. It
is a reproduction of committed repository content, not a capture of a
program run.

```sh
python3 tools/make_media.py
```

## Environment

| | |
|---|---|
| Machine | Apple silicon, macOS (Darwin 25.6.0) |
| Python | 3.11.5 |
| pip | 26.2.1 |
| Ollama | daemon 0.34.2 (running, none of the required models pulled) |
| PostgreSQL | none reachable |
| Pillow | 12.0.0 |
| Date | 2026-09-21 |

## Things deliberately not measured

| Quantity | Why not |
|---|---|
| Ingest wall-clock time per image | Vision model not available. |
| Query latency | No database, no embedding model. |
| Retrieval quality / recall | Would need a labelled query set; none exists. |
| Extraction accuracy as a score | n = 5, one run, unknown model build. Described qualitatively instead. |
| Actual `bge-m3` embedding width | Model not pulled. The mismatch with the hard-coded `embed_dim=1536` is discussed in [04 — Storage](04-storage.md) as a code-level observation, with the runtime width left unmeasured. |
