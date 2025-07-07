from fastapi import APIRouter
from server.controller.news_controller import NewsController

router = APIRouter(prefix="/news", tags=["news"])
controller = NewsController()

@router.get("/sync")
def sync_news():
    return controller.fetch_news()

