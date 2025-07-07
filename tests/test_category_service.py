import unittest
from unittest.mock import MagicMock
from server.services.category_service import CategoryService

class TestCategoryService(unittest.TestCase):
    def setUp(self):
        self.category_service = CategoryService()
        self.category_service.category_repo = MagicMock()

    def test_create_category_success(self):
        self.category_service.category_repo.find_category.return_value = None
        self.category_service.category_repo.create_category.return_value = {'name': 'Tech'}
        result = self.category_service.create_category('Tech')
        self.assertEqual(result['name'], 'Tech')

    def test_create_category_already_exists(self):
        self.category_service.category_repo.find_category.return_value = {'name': 'Tech'}
        with self.assertRaises(Exception):
            self.category_service.create_category('Tech')

    def test_set_category_visibility_success(self):
        self.category_service.category_repo.update_category_visibility.return_value = True
        result = self.category_service.set_category_visibility(1, True)
        self.assertTrue(result)

    def test_set_category_visibility_failure(self):
        self.category_service.category_repo.update_category_visibility.return_value = False
        with self.assertRaises(Exception):
            self.category_service.set_category_visibility(1, True)

    def test_get_all_categories_success(self):
        self.category_service.category_repo.get_all_categories.return_value = [{'name': 'Tech'}]
        result = self.category_service.get_all_categories()
        self.assertEqual(result, [{'name': 'Tech'}])

    def test_get_all_categories_failure(self):
        self.category_service.category_repo.get_all_categories.return_value = []
        with self.assertRaises(Exception):
            self.category_service.get_all_categories()

if __name__ == '__main__':
    unittest.main() 