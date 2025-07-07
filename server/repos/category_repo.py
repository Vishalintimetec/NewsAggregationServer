from server.core.database_connection import get_db_connection
from server.core.db_context import get_db_cursor

class CategoryRepo:
    def find_category(self, category_name):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT * FROM category WHERE category_name = %s", (category_name,))
            result = cursor.fetchone()
            return result

    def create_category(self, category_name):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("INSERT INTO category (category_name) VALUES (%s)", (category_name,))
            conn.commit()
        return self.find_category(category_name)

    def get_category_by_name(self, name: str):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT * FROM category WHERE category_name = %s", (name,))
            category = cursor.fetchone()
            return category

    def insert_article_category(self, category_id, article_id):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("insert into article_category_mapping(category_id, article_id) values(%s,%s)",
                           (category_id, article_id))
            conn.commit()

    def update_category_visibility(self, category_id: int, is_visible):
        with get_db_cursor() as (conn, cursor):
            cursor.execute("""
                UPDATE category SET is_visible = %s WHERE category_id = %s
            """, (is_visible, category_id))
            conn.commit()
            return {"message": "Category visibility updated"}

    def get_category_id_by_name(self, name: str):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT category_id FROM category WHERE category_name = %s", (name,))
            result = cursor.fetchone()
            return result["category_id"] if result else None


    def get_all_categories(self):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT category_id, category_name FROM category order by category_id")
            categories = cursor.fetchall()
            return categories

