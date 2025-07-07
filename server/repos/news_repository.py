from server.core.database_connection import get_db_connection
from server.schemas.news import NewsArticleCreate
from datetime import datetime
from server.core.db_context import get_db_cursor

class NewsRepository:
    def save(self, news: NewsArticleCreate):
        with get_db_cursor() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO articles (server_id, title, description, content, source, url, published_at, fetched_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    news.server_id,
                    news.title,
                    news.description,
                    news.content,
                    news.source,
                    news.url,
                    news.published_at,
                    datetime.now()
                )
            )
            conn.commit()
            article_id = cursor.lastrowid
            return article_id

    def find_latest_article_id(self):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT article_id FROM articles ORDER BY article_id DESC LIMIT 1")
            result = cursor.fetchone()
            return result
