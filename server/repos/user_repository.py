from server.utils.password_utils import hash_password
from server.core.db_context import get_db_cursor

class UserRepository:

    def get_user_by_id(self, user_id: int):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            return user

    def get_user_by_email(self, email: str):
        with get_db_cursor(dictionary=True) as (conn, cursor):
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user

    def create(self, user):
        with get_db_cursor() as (conn, cursor):
            hashed_password = hash_password(user.password)
            cursor.execute(
                "INSERT INTO users (username, email, password, user_role) VALUES (%s, %s, %s, %s)",
                (user.username, user.email, hashed_password, user.role)
            )
            conn.commit()
        # Return the created user (fetch again)
        return self.get_user_by_email(user.email)