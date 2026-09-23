#!/usr/bin/env python3
"""Print the PostgreSQL table cookingRAG creates, without needing a server.

util/database_conection.py hands table_name="recipes" and embed_dim=1536 to
PGVectorStore. The table that llama_index then creates is not called "recipes"
and its columns are not obvious from the call site, so this script compiles the
SQLAlchemy model llama_index would use and prints the DDL for the PostgreSQL
dialect.

    python3 tools/show_schema.py

Requires the project dependencies. No database connection is made.
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)


def main():
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.orm import declarative_base
    from sqlalchemy.schema import CreateTable
    from llama_index.vector_stores.postgres.base import get_data_model

    import util.database_conection as dbc

    table_name = "recipes"   # util/database_conection.py:58
    embed_dim = 1536         # util/database_conection.py:59
    schema_name = "public"   # PGVectorStore.from_params default

    print("Parameters taken from util/database_conection.py:")
    print("    table_name = %r" % table_name)
    print("    embed_dim  = %r" % embed_dim)
    print("    schema     = %r  (from_params default)" % schema_name)
    print("    database   = %r  (PG_DB_NAME)" % dbc.db_name)
    print()

    model = get_data_model(
        declarative_base(), table_name, schema_name,
        hybrid_search=False, text_search_config="english",
        cache_okay=False, embed_dim=embed_dim, use_jsonb=False,
    )

    print("Resulting table: %s.%s" % (schema_name, model.__tablename__))
    print()
    print(CreateTable(model.__table__).compile(dialect=postgresql.dialect()))
    print("Plus, issued separately by PGVectorStore before the table is made:")
    print()
    print("    CREATE EXTENSION IF NOT EXISTS vector;")
    print()
    print("No HNSW or IVFFlat index is created: hnsw_kwargs is not passed, so")
    print("similarity search runs as a sequential scan with cosine distance.")


if __name__ == "__main__":
    main()
