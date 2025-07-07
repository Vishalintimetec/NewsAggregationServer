from server.core.db_context import get_db_cursor

class CategoryArticleMappingRepo:
    def create_article_category_mapping(self, category_id, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute(
                "INSERT INTO category_article_mapping (category_id, article_id) VALUES (%s, %s)",
                (category_id, article_id)
            )
            conn.commit()
