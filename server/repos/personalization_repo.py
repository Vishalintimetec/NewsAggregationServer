from server.core.db_context import get_db_cursor
class PersonalizationRepo:

    def get_user_category_counts(self, user_id):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT c.category_name, SUM(cnt) as total_count
                FROM (
                    SELECT acm.category_id, COUNT(*) as cnt
                    FROM article_preferences ap
                    JOIN article_category_mapping acm ON ap.article_id = acm.article_id
                    WHERE ap.user_id = %s
                    GROUP BY acm.category_id

                    UNION ALL

                    SELECT acm.category_id, COUNT(*) as cnt
                    FROM user_article_view_history rh
                    JOIN article_category_mapping acm ON rh.article_id = acm.article_id
                    WHERE rh.user_id = %s
                    GROUP BY acm.category_id

                    UNION ALL

                    SELECT acm.category_id, COUNT(*) as cnt
                    FROM saved_article sa
                    JOIN article_category_mapping acm ON sa.article_id = acm.article_id
                    WHERE sa.user_id = %s
                    GROUP BY acm.category_id

                    UNION ALL

                    SELECT np.category_id, COUNT(*) as cnt
                    FROM notification_preferences np
                    WHERE np.user_id = %s AND np.is_enabled = TRUE
                    GROUP BY np.category_id

                    UNION ALL

                    SELECT uns.category_id, COUNT(*) as cnt
                    FROM notification_preferences uns
                    WHERE uns.user_id = %s AND uns.is_enabled = TRUE
                    GROUP BY uns.category_id
                ) as all_cats
                JOIN category c ON all_cats.category_id = c.category_id
                GROUP BY c.category_name
                ORDER BY total_count DESC
            """, (user_id, user_id, user_id, user_id, user_id))
            result = cursor.fetchall()
            return {row['category_name']: row['total_count'] for row in result}

    # def get_articles_by_preference(self, user_id, preference):
    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute(
    #         "SELECT article_id FROM article_preferences WHERE user_id = %s AND preference = %s",
    #         (user_id, preference)
    #     )
    #     articles = [row["article_id"] for row in cursor.fetchall()]
    #     cursor.close()
    #     conn.close()
    #     return articles

    # def get_saved_articles(self, user_id):
    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute("SELECT article_id FROM saved_articles WHERE user_id = %s", (user_id,))
    #     saved = [row["article_id"] for row in cursor.fetchall()]
    #     cursor.close()
    #     conn.close()
    #     return saved
    #
    # def get_read_history(self, user_id):
    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute("SELECT article_id FROM read_history WHERE user_id = %s", (user_id,))
    #     read = [row["article_id"] for row in cursor.fetchall()]
    #     cursor.close()
    #     conn.close()
    #     return read
    #
    # def get_notification_preferences(self, user_id):
    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute("""
    #         SELECT c.category_name, np.is_enabled, np.keyword
    #         FROM notification_preferences np
    #         JOIN category c ON np.category_id = c.category_id
    #         WHERE np.user_id = %s
    #     """, (user_id,))
    #     prefs = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     # Return as a dict: {category_name: {'is_enabled': bool, 'keyword': str or None}}
    #     return {row['category_name']: {'is_enabled': row['is_enabled'], 'keyword': row['keyword']} for row in prefs}