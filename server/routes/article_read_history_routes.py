from fastapi import APIRouter, Depends
from server.controller.article_read_history_controller import ArticleReadHistoryController
from server.core.jwt_utils import get_current_user

router = APIRouter(prefix="/read-history", tags=["read-history"])
controller = ArticleReadHistoryController()

@router.post("/read/{article_id}")
def record_read(article_id: int, user=Depends(get_current_user)):
    return controller.record_read(user['user_id'], article_id)

@router.get("/read-history")
def get_read_history(user=Depends(get_current_user)):
    return controller.get_read_history(user['user_id'])