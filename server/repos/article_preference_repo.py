from server.core.db_context import get_db_cursor

class ArticlePreferenceRepo:
    def set_preference(self, user_id, article_id, preference):
        with get_db_cursor() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO article_preferences (user_id, article_id, preference)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE preference = VALUES(preference)
                """,
                (user_id, article_id, preference)
            )
            conn.commit()
            return {"message": f"Article with article_id {article_id} is {preference}d successfully."}