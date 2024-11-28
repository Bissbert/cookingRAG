import os
import psycopg2
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext

# Database connection details
PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_PORT = os.environ.get('PG_PORT', '5432')
PG_USER = os.environ.get('PG_USER', 'postgres')
PG_PASSWORD = os.environ.get('PG_PASSWORD', 'your_database_password')  # Replace with your password or use environment variable
PG_DB_NAME = os.environ.get('PG_DB_NAME', 'recipe_db')

connection_string = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}"
db_name = PG_DB_NAME

def setup_database():
    conn = psycopg2.connect(connection_string)
    conn.autocommit = True
    with conn.cursor() as c:
        # Create the database if it doesn't exist
        c.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = c.fetchone()
        if not exists:
            c.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")
    conn.close()

def setup_vector_store():
    vector_store = PGVectorStore.from_params(
        database=db_name,
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        table_name="recipes",
        embed_dim=1536,  # Adjust based on your embedding model
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context
