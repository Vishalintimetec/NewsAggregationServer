from fastapi import HTTPException

from server.repos.category_repo import CategoryRepo


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepo()

    def create_category(self, category_name):
        existing = self.category_repo.find_category(category_name)
        if existing:
            raise HTTPException(status_code=400, detail=f"Category '{category_name}' already exists")
        return self.category_repo.create_category(category_name)

    def set_category_visibility(self, category_id: int, is_visible):
        return self.category_repo.update_category_visibility(category_id, is_visible)

    def get_all_categories(self):
        return self.category_repo.get_all_categories()
