from server.core.database_connection import get_db_connection
from server.schemas.article_search import SearchArticleRequest
from server.core.db_context import get_db_cursor

class ArticleRepository:

    def fetch_headlines_by_day(self):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT a.*, c.category_name
                FROM articles a
                JOIN article_category_mapping acm ON a.article_id = acm.article_id
                JOIN category c ON acm.category_id = c.category_id
                WHERE DATE(a.published_at) = CURDATE()
                  AND c.is_visible = TRUE
                  AND a.is_visible = TRUE
            """)
            result = cursor.fetchall()
            return result

    def fetch_headlines_in_range(self, start, end, category):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            if category:
                cursor.execute("""
                    SELECT a.*, c.category_name
                    FROM articles a
                    JOIN article_category_mapping acm ON a.article_id = acm.article_id
                    JOIN category c ON acm.category_id = c.category_id
                    WHERE a.published_at BETWEEN %s AND %s
                      AND c.category_name = %s
                      AND c.is_visible = TRUE
                      AND a.is_visible = TRUE
                """, (start, end, category))
            else:
                cursor.execute("""
                    SELECT a.*, c.category_name
                    FROM articles a
                    JOIN article_category_mapping acm ON a.article_id = acm.article_id
                    JOIN category c ON acm.category_id = c.category_id
                    WHERE a.published_at BETWEEN %s AND %s
                      AND c.is_visible = TRUE
                      AND a.is_visible = TRUE
                """, (start, end))
            result = cursor.fetchall()
            return result

    def fetch_saved_articles(self, user_id):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT DISTINCT na.*
                FROM saved_article sa
                JOIN articles na ON sa.article_id = na.article_id
                JOIN article_category_mapping acm ON na.article_id = acm.article_id
                JOIN category c ON acm.category_id = c.category_id
                WHERE sa.user_id = %s
                  AND na.is_visible = TRUE
                  AND c.is_visible = TRUE
            """, (user_id,))
            result = cursor.fetchall()
            return result

    def insert_saved_article(self, user_id, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("INSERT INTO saved_article (user_id, article_id) VALUES (%s, %s)", (user_id, article_id))
            conn.commit()
            return {"message": "Article saved."}

    def remove_saved_article(self, user_id, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("DELETE FROM saved_article WHERE user_id = %s AND article_id = %s", (user_id, article_id))
            conn.commit()
            return {"message": "Article deleted."}

    def get_news_by_keyword(self, search_request: SearchArticleRequest):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            keyword = f"%{search_request.keyword}%"
            start_date = search_request.start_date
            end_date = search_request.end_date
            query = """
                SELECT a.article_id, title, description, content, source, url, published_at, c.category_name
                FROM articles a
                JOIN article_category_mapping acm ON a.article_id = acm.article_id
                JOIN category c ON acm.category_id = c.category_id 
                WHERE c.is_visible = TRUE
                  AND a.is_visible = TRUE
                  AND CONCAT_WS(' ', title, description, content) LIKE %s
            """
            params = [keyword]
            if start_date and end_date:
                query += " AND DATE(published_at) >= %s AND DATE(published_at) <= %s"
                params += [start_date, end_date]
            cursor.execute(query, tuple(params))
            result = cursor.fetchall()
            return result

    def hide_article(self, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                   UPDATE articles SET is_visible = FALSE WHERE article_id = %s
               """, (article_id,))
            conn.commit()
            return {"message": f"Article with article_id {article_id} is hidden successfully."}

    def unhide_article(self, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                   UPDATE articles SET is_visible = TRUE WHERE article_id = %s
               """, (article_id,))
            conn.commit()
            return {"message": f"Article with article_id {article_id} is unhidden successfully."}

