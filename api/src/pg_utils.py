import os
import psycopg2
import dotenv

from psycopg2.extensions import connection, cursor

# dotenv.load_dotenv("environments/postgres.env")


def get_connection() -> connection:
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )


def get_group_by_collection(cursor: cursor, collection: str) -> int | None:
    cursor.execute(
        "SELECT * FROM protected_gropes WHERE collection_address = %s",
        (collection,)
    )

    res = cursor.fetchone()
    return res[1] if res is not None else None


def get_user_wallet_by_id(cursor: cursor, user_id: int) -> str | None:
    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (user_id,)
    )

    res = cursor.fetchone()
    return res[2] if res is not None else None
