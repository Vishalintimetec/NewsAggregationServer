from server.core.database_connection import get_db_connection
from server.core.db_context import get_db_cursor

class BlockedKeywordRepo:
    def block_keyword(self, keyword):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("INSERT IGNORE INTO blocked_keywords (keyword) VALUES (%s)", (keyword,))
            conn.commit()
            return {"message": "Keyword blocked."}

    def unblock_keyword(self, keyword):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("DELETE FROM blocked_keywords WHERE keyword = %s", (keyword,))
            conn.commit()
            return {"message": "Keyword unblocked."}

    def get_all_keywords(self):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT keyword FROM blocked_keywords")
            keywords = [row["keyword"] for row in cursor.fetchall()]
            return keywords