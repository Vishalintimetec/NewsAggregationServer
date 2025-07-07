from server.core.db_context import get_db_cursor

class SavedArticleRepository:
    def get_by_user(self, user_id: int):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute(
                "SELECT a.* FROM saved_articles s JOIN article a ON s.article_id = a.article_id WHERE s.user_id = %s",
                (user_id,))
            result = cursor.fetchall()
            return result
