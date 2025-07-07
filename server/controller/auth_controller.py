from fastapi import HTTPException

from server.config.http_status_codes import HTTP_BAD_REQUEST
from server.services.authentication_service import AuthenticationService
from server.schemas.user import UserCreate
from server.schemas.auth import UserCredentials


class AuthController:
    def __init__(self):
        self.auth_service = AuthenticationService()

    def login(self, user_data: UserCredentials):
        return self.auth_service.login(user_data)

    def register(self, user: UserCreate):
        db_user = self.auth_service.register_user(user)
        return db_user