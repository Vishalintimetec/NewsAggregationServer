from pydantic import BaseModel

class KeywordRequest(BaseModel):
    keyword: str