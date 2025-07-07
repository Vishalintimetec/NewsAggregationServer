from server.core.database_connection import get_db_connection
from server.core.db_context import get_db_cursor

class ReportManager:

    def report_article(self, article_id, user_id, reason):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                INSERT IGNORE INTO reports (article_id, user_id, reason)
                VALUES (%s, %s, %s)
            """, (article_id, user_id, reason))
            conn.commit()

    def get_report_count(self, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                SELECT COUNT(*) FROM reports WHERE article_id = %s
            """, (article_id,))
            count = cursor.fetchone()[0]
            return count

    def get_reported_articles(self):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("""
                SELECT article_id, count(*) as reported_count
                from reports 
                group by article_id
                order by reported_count
            """)
            results = cursor.fetchall()
            return results

