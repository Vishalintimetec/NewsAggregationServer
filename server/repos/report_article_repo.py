from server.core.database_connection import get_db_connection


class ReportManager:

    def report_article(self, article_id, user_id, reason):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT IGNORE INTO reports (article_id, user_id, reason)
            VALUES (%s, %s, %s)
        """, (article_id, user_id, reason))
        conn.commit()
        cursor.close()
        conn.close()

    def get_report_count(self, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM reports WHERE article_id = %s
        """, (article_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def get_reported_articles(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT article_id, count(*) as reported_count
            from reports 
            group by article_id
            order by reported_count
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

