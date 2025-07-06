from server.core.database_connection import get_db_connection

class ReadHistoryRepo:
    def add_read_history(self, user_id, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT IGNORE INTO user_article_view_history (user_id, article_id) VALUES (%s, %s)",
            (user_id, article_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Read history recorded."}

    def get_read_history(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT article_id FROM user_article_view_history WHERE user_id = %s", (user_id,))
        read = [row["article_id"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return read