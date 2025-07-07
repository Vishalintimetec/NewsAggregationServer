import unittest
from unittest.mock import patch, MagicMock
from server.services.news_service import NewsService

class TestNewsService(unittest.TestCase):
    def setUp(self):
        self.news_service = NewsService()
        self.news_service.news_repo = MagicMock()
        self.news_service.api_manager = MagicMock()
        self.news_service.category_repo = MagicMock()
        self.news_service.classifier = MagicMock()
        self.news_service.notification_service = MagicMock()

    @patch('server.services.news_service.requests.get')
    def test_fetch_news_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'articles': [1, 2, 3]}
        result = self.news_service.fetch_news('http://fakeurl')
        self.assertEqual(result, {'articles': [1, 2, 3]})

    @patch('server.services.news_service.requests.get')
    def test_fetch_news_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        result = self.news_service.fetch_news('http://fakeurl')
        self.assertIsNone(result)

    def test_fetch_news_from_api_no_apis(self):
        self.news_service.api_manager.get_all_server_details.return_value = []
        result = self.news_service.fetch_news_from_api()
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main() 