from server.core.db_context import get_db_cursor

class ReadHistoryRepo:
    def add_read_history(self, user_id, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute(
                "INSERT IGNORE INTO user_article_view_history (user_id, article_id) VALUES (%s, %s)",
                (user_id, article_id)
            )
            conn.commit()
            return {"message": "Read history recorded."}

    def get_read_history(self, user_id):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT article_id FROM user_article_view_history WHERE user_id = %s", (user_id,))
            read = [row["article_id"] for row in cursor.fetchall()]
            return read