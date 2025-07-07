from fastapi import HTTPException
from server.Exceptions.category_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException
from server.repos.category_repo import CategoryRepo


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepo()

    def create_category(self, category_name):
        existing = self.category_repo.find_category(category_name)
        if existing:
            raise CategoryAlreadyExistsException(f"Category '{category_name}' already exists")
        return self.category_repo.create_category(category_name)

    def set_category_visibility(self, category_id: int, is_visible):
        result = self.category_repo.update_category_visibility(category_id, is_visible)
        if not result:
            raise CategoryNotFoundException(f"Category with id {category_id} not found")
        return result

    def get_all_categories(self):
        categories = self.category_repo.get_all_categories()
        if not categories:
            raise CategoryNotFoundException("No categories found")
        return categories
