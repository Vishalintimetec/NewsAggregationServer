from pydantic import BaseModel

class CategoryVisibilityUpdate(BaseModel):
    is_visible : bool
