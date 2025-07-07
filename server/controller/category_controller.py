# from fastapi import HTTPException
from server.services.category_service import CategoryService
from server.schemas.category import CategoryCreate
# from Exceptions.exceptions import CategoryNotFoundException
# from config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND
# from typing import List

class CategoryController:
    def __init__(self):
        self.category_service = CategoryService()

    def create_category(self, category: CategoryCreate):
        return self.category_service.create_category(category.name)

    def toggle_category_visibility(self, category_id: int, is_visible):
        return self.category_service.set_category_visibility(category_id, is_visible)

    def get_all_categories(self):
        return self.category_service.get_all_categories()
