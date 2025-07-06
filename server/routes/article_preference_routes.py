from fastapi import APIRouter, Depends
from server.controller.article_preference_controller import ArticlePreferenceController
from server.core.jwt_utils import get_current_user

router = APIRouter(prefix="/preferences", tags=["preferences"])
controller = ArticlePreferenceController()

@router.post("/like/{article_id}")
def like_article(article_id: int, user=Depends(get_current_user)):
    return controller.like_article(user['user_id'], article_id)

@router.post("/dislike/{article_id}")
def dislike_article(article_id: int, user=Depends(get_current_user)):
    return controller.dislike_article(user['user_id'], article_id)