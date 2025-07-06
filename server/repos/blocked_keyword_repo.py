from server.core.database_connection import get_db_connection

class BlockedKeywordRepo:
    def block_keyword(self, keyword):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO blocked_keywords (keyword) VALUES (%s)", (keyword,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Keyword blocked."}

    def unblock_keyword(self, keyword):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blocked_keywords WHERE keyword = %s", (keyword,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Keyword unblocked."}

    def get_all_keywords(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT keyword FROM blocked_keywords")
        keywords = [row["keyword"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return keywords