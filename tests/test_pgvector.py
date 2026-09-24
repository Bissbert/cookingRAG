"""End to end against a real pgvector server, with fake Ollama models.

Ingests recipes through ingest_recipes.process_recipe_images() into a fresh
database, then answers a question through query_recipes.main(). Covers #7 (the
table must be created in a new database), #6 (the column must accept
bge-m3-width vectors) and #5 (the query must run on the local models with no
OpenAI key). Skipped when PG_HOST is not set.
"""

import os
import uuid

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("PG_HOST"), reason="needs a pgvector server (PG_HOST)"
)

from conftest import BGE_M3_DIM, FAKE_ANSWER


def recipes():
    from util.recipe import Recipe

    return [
        Recipe(
            title="Red lentil soup",
            ingredients=["200 g red lentils", "1 onion", "1 l vegetable stock"],
            instructionsAsString="Soften the onion, add lentils and stock, simmer 20 minutes.",
            cook_time="30 minutes",
            type="cooking",
            dietary_preference="vegan",
        ),
        Recipe(
            title="Butter cake",
            ingredients=["250 g butter", "250 g sugar", "4 eggs", "250 g flour"],
            instructionsAsString="Cream butter and sugar, beat in eggs, fold in flour, bake 50 minutes.",
            cook_time="60 minutes",
            type="baking",
            dietary_preference="vegetarian",
        ),
    ]


@pytest.fixture
def fresh_db(monkeypatch, tmp_path):
    """A new database per test, created by the project's own setup_database()."""
    import util.database_conection as dbc

    name = "cr_test_" + uuid.uuid4().hex[:8]
    monkeypatch.setattr(dbc, "db_name", name)
    monkeypatch.chdir(tmp_path)  # save_data_objects_to_json writes to cwd
    dbc.setup_database()
    return name


def ingest(monkeypatch, tmp_path):
    import asyncio
    import ingest_recipes
    from util.embedding_util import initEmbeddingModel
    from util.database_conection import setup_vector_store

    (tmp_path / "img.jpg").write_bytes(b"")

    async def fake_extract(files):
        return recipes()

    monkeypatch.setattr(ingest_recipes, "aprocess_image_files", fake_extract)
    initEmbeddingModel()
    asyncio.run(ingest_recipes.process_recipe_images(str(tmp_path), setup_vector_store()))


def column_width(db_name):
    import psycopg2
    import util.database_conection as dbc

    conn = psycopg2.connect(
        host=dbc.PG_HOST, port=dbc.PG_PORT, user=dbc.PG_USER,
        password=dbc.PG_PASSWORD, dbname=db_name,
    )
    with conn, conn.cursor() as c:
        c.execute(
            "SELECT format_type(atttypid, atttypmod) FROM pg_attribute "
            "WHERE attrelid = 'public.data_recipes'::regclass AND attname = 'embedding'"
        )
        width = c.fetchone()[0]
        c.execute("SELECT count(*) FROM public.data_recipes")
        rows = c.fetchone()[0]
    conn.close()
    return width, rows


def test_store_setup_creates_the_table_in_a_new_database(fresh_db):
    """#7: llama-index-vector-stores-postgres 0.3.1 skipped this when 'public' existed."""
    from util.database_conection import setup_vector_store

    setup_vector_store().vector_store._initialize()
    width, rows = column_width(fresh_db)
    assert width == "vector(%d)" % BGE_M3_DIM
    assert rows == 0


def test_ingest_stores_bge_m3_width_vectors(monkeypatch, tmp_path, fresh_db, fake_ollama):
    ingest(monkeypatch, tmp_path)
    width, rows = column_width(fresh_db)
    assert width == "vector(%d)" % BGE_M3_DIM
    assert rows == 2
    assert set(fake_ollama["embed_models"]) == {"bge-m3"}


def test_query_answers_locally_from_the_ingested_store(monkeypatch, tmp_path, fresh_db, fake_ollama, capsys):
    import query_recipes

    ingest(monkeypatch, tmp_path)
    capsys.readouterr()
    fake_ollama["embed_models"].clear()

    monkeypatch.setattr("sys.argv", ["query_recipes.py", "something", "vegan", "with", "lentils"])
    query_recipes.main()

    out = capsys.readouterr().out
    assert "Search Results:" in out
    assert FAKE_ANSWER in out
    assert fake_ollama["embed_models"] == ["bge-m3"]  # the question, with the ingest model
    assert fake_ollama["llm_models"] == ["qwq"]
