from contextlib import contextmanager
from server.core.database_connection import get_db_connection
import mysql.connector

@contextmanager
def get_db_cursor(dictionary=False):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=dictionary)
        yield conn, cursor
    except mysql.connector.Error as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()