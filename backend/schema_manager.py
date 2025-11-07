# schema_manager.py
import sqlite3
import sqlalchemy
import os

TEMP_DB = "/app/schema_memory.db"   # stored INSIDE container

def refresh_schema(main_db_url: str):
    engine = sqlalchemy.create_engine(main_db_url)
    inspector = sqlalchemy.inspect(engine)

    conn = sqlite3.connect(TEMP_DB)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS schema_memory")
    cursor.execute("""
        CREATE TABLE schema_memory (
            table_name TEXT,
            column_name TEXT
        )
    """)

    for table in inspector.get_table_names():
        for col in inspector.get_columns(table):
            cursor.execute(
                "INSERT INTO schema_memory (table_name, column_name) VALUES (?, ?)",
                (table, col["name"])
            )

    conn.commit()
    conn.close()


def get_schema():
    conn = sqlite3.connect(TEMP_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT table_name, column_name FROM schema_memory")
    rows = cursor.fetchall()
    conn.close()

    schema = {}
    for table, col in rows:
        schema.setdefault(table, []).append(col)

    return "\n".join(
        f"- {table}: {', '.join(cols)}"
        for table, cols in schema.items()
    )
