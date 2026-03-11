from app.db.connection import get_connection


def get_db():
    """
    FastAPI dependency that provides a database connection.
    Guarantees connection is closed after the request completes,
    even if an exception occurs.
    """

    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
