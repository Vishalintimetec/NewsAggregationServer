import unittest
from unittest.mock import MagicMock
from server.services.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user_service.repo = MagicMock()
        self.user_service.user_repo = MagicMock()
        self.user_service.blocked_keyword_service = MagicMock()
        self.user_service.personalization_repo = MagicMock()

    def test_get_user_by_id(self):
        self.user_service.user_repo.get_user_by_id.return_value = {'id': 1, 'name': 'John'}
        user = self.user_service.get_user_by_id(1)
        self.assertEqual(user['name'], 'John')

    def test_filter_blocked_articles(self):
        self.user_service.blocked_keyword_service.get_all_keywords.return_value = ['bad']
        articles = [
            {'title': 'Good News', 'content': 'All good'},
            {'title': 'Bad News', 'content': 'Something bad happened'}
        ]
        filtered = self.user_service.filter_blocked_articles(articles)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['title'], 'Good News')

    def test_get_headlines_today(self):
        self.user_service.repo.fetch_headlines_by_day.return_value = [
            {'title': 'Headline', 'content': 'Content'}
        ]
        self.user_service.blocked_keyword_service.get_all_keywords.return_value = []
        self.user_service.personalization_repo.get_user_category_counts.return_value = {}
        result = self.user_service.get_headlines_today(1)
        self.assertIsInstance(result, list)

    def test_save_article(self):
        self.user_service.repo.insert_saved_article.return_value = True
        result = self.user_service.save_article(1, 101)
        self.assertTrue(result)

    def test_delete_article(self):
        self.user_service.repo.remove_saved_article.return_value = True
        result = self.user_service.delete_article(1, 101)
        self.assertTrue(result)

    def test_logout(self):
        result = self.user_service.logout(1)
        self.assertEqual(result['message'], 'User 1 logged out successfully.')

if __name__ == '__main__':
    unittest.main() 