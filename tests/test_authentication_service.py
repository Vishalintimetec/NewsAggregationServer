import unittest
from unittest.mock import MagicMock, patch
from server.services.authentication_service import AuthenticationService
from server.schemas.user import UserCreate
from server.schemas.auth import UserCredentials

class TestAuthenticationService(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthenticationService()
        self.auth_service.user_repo = MagicMock()

    def test_register_user_success(self):
        self.auth_service.user_repo.get_user_by_email.return_value = None
        self.auth_service.user_repo.create.return_value = {'user_id': 1, 'email': 'test@example.com'}
        user = UserCreate(email='test@example.com', password='pass', name='Test', user_role='user')
        result = self.auth_service.register_user(user)
        self.assertEqual(result['email'], 'test@example.com')

    def test_register_user_already_exists(self):
        self.auth_service.user_repo.get_user_by_email.return_value = {'email': 'test@example.com'}
        user = UserCreate(email='test@example.com', password='pass', name='Test', user_role='user')
        with self.assertRaises(ValueError):
            self.auth_service.register_user(user)

    @patch('server.services.authentication_service.verify_password')
    @patch('server.services.authentication_service.create_access_token')
    def test_login_success(self, mock_create_token, mock_verify):
        self.auth_service.user_repo.get_user_by_email.return_value = {
            'email': 'test@example.com', 'password': 'hashed', 'user_id': 1, 'user_role': 'user'
        }
        mock_verify.return_value = True
        mock_create_token.return_value = 'token123'
        creds = UserCredentials(email='test@example.com', password='pass')
        result = self.auth_service.login(creds)
        self.assertEqual(result['access_token'], 'token123')
        self.assertEqual(result['email'], 'test@example.com')

    def test_login_wrong_email(self):
        self.auth_service.user_repo.get_user_by_email.return_value = None
        creds = UserCredentials(email='wrong@example.com', password='pass')
        with self.assertRaises(ValueError):
            self.auth_service.login(creds)


if __name__ == '__main__':
    unittest.main() 