from server.core.database_connection import get_db_connection

class ArticleRepository:

    def fetch_headlines_by_day(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

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
        cursor.close()
        conn.close()
        return result

    def fetch_headlines_in_range(self, start, end, category):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

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
        cursor.close()
        conn.close()
        return result

    def fetch_saved_articles(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
        cursor.close()
        conn.close()
        return result

    def insert_saved_article(self, user_id, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saved_article (user_id, article_id) VALUES (%s, %s)", (user_id, article_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Article saved."}

    def remove_saved_article(self, user_id, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_article WHERE user_id = %s AND article_id = %s", (user_id, article_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Article deleted."}

    def search_articles(self, query, start, end, sort_by):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT DISTINCT a.*, c.category_name
            FROM articles a
            JOIN article_category_mapping acm ON a.article_id = acm.article_id
            JOIN category c ON acm.category_id = c.category_id
            WHERE (a.title LIKE %s OR a.description LIKE %s)
              AND a.is_visible = TRUE
              AND c.is_visible = TRUE
        """
        params = [f"%{query}%", f"%{query}%"]

        if start and end:
            sql += " AND a.published_at BETWEEN %s AND %s"
            params += [start, end]

        if sort_by in ["likes", "dislikes"]:
            sql += f" ORDER BY a.{sort_by} DESC"

        cursor.execute(sql, tuple(params))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def hide_article(self, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
               UPDATE articles SET is_visible = FALSE WHERE article_id = %s
           """, (article_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Article with article_id {article_id} is hidden successfully."}

    def unhide_article(self, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
               UPDATE articles SET is_visible = TRUE WHERE article_id = %s
           """, (article_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Article with article_id {article_id} is unhidden successfully."}

