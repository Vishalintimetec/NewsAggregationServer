from pydantic import BaseModel

class ReportArticleRequest(BaseModel):
    article_id: int
