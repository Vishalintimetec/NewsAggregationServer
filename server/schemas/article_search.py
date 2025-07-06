from pydantic import BaseModel
from typing import Optional

class SearchArticleRequest(BaseModel):
    keyword: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None