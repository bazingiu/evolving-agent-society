import os

from langgraph.checkpoint.memory import MemorySaver


def get_checkpointer():
    """
    While developing (without POSTGRES_URL) uses MemorySaver — in memory, resets on restart.
    While producing with POSTGRES_URL uses PostgresSaver — persistent between restarts.
    """
    db_url = os.getenv("POSTGRES_URL")

    if db_url:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver

            return PostgresSaver.from_conn_string(db_url)
        except ImportError:
            print("⚠️  psycopg not installed, fallback to MemorySaver")

    return MemorySaver()
