from server.core.database_connection import get_db_connection

class ArticlePreferenceRepo:
    def set_preference(self, user_id, article_id, preference):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Upsert: if exists, update; else, insert
        cursor.execute(
            """
            INSERT INTO article_preferences (user_id, article_id, preference)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE preference = VALUES(preference)
            """,
            (user_id, article_id, preference)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Article with article_id {article_id} is {preference}d successfully."}