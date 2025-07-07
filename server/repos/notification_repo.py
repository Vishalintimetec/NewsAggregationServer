from server.core.database_connection import get_db_connection
from server.repos.category_repo import CategoryRepo
from server.core.db_context import get_db_cursor

category_repo = CategoryRepo()
class NotificationRepo:

    def insert_preference(self, user_id, preference_data):
        category_id = category_repo.get_category_id_by_name(preference_data.category)
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                            INSERT INTO notification_preferences (user_id, category_id, keyword)
                            VALUES (%s, %s, %s)
                        """, (user_id, category_id, preference_data.keyword))
            conn.commit()
            preference_id = cursor.lastrowid
            return {"Notification added successfully"}

    def get_preferences_by_user(self, user_id):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                    SELECT 
                        np.id, 
                        np.user_id, 
                        c.category_name AS category, 
                        np.is_enabled, 
                        np.keyword
                    FROM notification_preferences np
                    JOIN category c ON np.category_id = c.category_id
                    WHERE np.user_id = %s
                """, (user_id,))
            preferences = cursor.fetchall()
            return preferences

    def configure_notifications(self, user_id, config_data):
        with get_db_cursor() as (conn, cursor):
            for config in config_data:
                category_id = config['category_id']
                is_enabled = config['is_enabled']
                keywords = config['keywords']

                if is_enabled and keywords:
                    for keyword in keywords:
                        cursor.execute("""
                            INSERT INTO notification_preferences (user_id, category_id, is_enabled, keyword)
                            VALUES (%s, %s, %s, %s)
                        """, (user_id, category_id, 1, keyword))
                elif is_enabled:
                    cursor.execute("""
                        INSERT INTO notification_preferences (user_id, category_id, is_enabled, keyword)
                        VALUES (%s, %s, %s, NULL)
                    """, (user_id, category_id, 1))
                else:
                    cursor.execute("""
                                UPDATE notification_preferences
                                SET is_enabled = 0
                                WHERE user_id = %s AND category_id = %s
                            """, (user_id, category_id))
            conn.commit()
            return {"message": "Notification preferences configured successfully."}

    def delete_preference(self, user_id, pref_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("DELETE FROM notification_preferences WHERE id = %s AND user_id = %s", (pref_id, user_id))
            conn.commit()
            return {"detail": "Preference deleted"}

    def insert_notifications_for_new_articles(self):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                INSERT IGNORE INTO notifications (user_id, article_id, message)
                SELECT t1.user_id, t3.article_id, t3.title
                FROM notification_preferences t1
                JOIN article_category_mapping t2 ON t1.category_id = t2.category_id
                JOIN articles t3 ON t3.article_id = t2.article_id
                WHERE 
                    (t1.keyword IS NULL OR 
                    CONCAT_WS(' ', t3.title, t3.description, t3.content) LIKE CONCAT('%', t1.keyword, '%'))
                    AND t3.fetched_at >= NOW() - INTERVAL 4 HOUR;
            """)
            conn.commit()

    def get_unread_notifications_grouped_by_user(self):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT u.email, u.user_id, 
                    GROUP_CONCAT(CONCAT('Title - ', n.message, '\nURL   - ', a.url, '\n') SEPARATOR '\n') AS messages
                FROM notifications n
                JOIN users u ON u.user_id = n.user_id
                JOIN articles a ON a.article_id = n.article_id
                WHERE n.is_read = 0
                GROUP BY u.user_id
            """)
            results = cursor.fetchall()
            return results

    def get_unread_notifications(self, user_id):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                  SELECT id, article_id, message, created_at
                  FROM notifications
                  WHERE user_id = %s AND is_read = 0
                  ORDER BY created_at DESC
              """, (user_id,))
            notifications = cursor.fetchall()
            return notifications

    # def mark_all_notifications_as_read(self):
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("UPDATE notification SET is_read = 1 WHERE is_read = 0")
    #     conn.commit()
    #     cursor.close()
    #     conn.close()

    def mark_notification_as_read(self, user_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                  UPDATE notifications
                  SET is_read = 1
                  WHERE user_id = %s AND is_read = 0
              """, (user_id,))
            conn.commit()
            return {"message": "Notification marked as read."}