from fastapi import APIRouter, Depends, HTTPException
from server.controller.article_preference_controller import ArticlePreferenceController
from server.core.jwt_utils import get_current_user
from server.Exceptions.article_exceptions import ArticleNotFoundException

router = APIRouter(prefix="/preferences", tags=["preferences"])
controller = ArticlePreferenceController()

@router.post("/like/{article_id}")
def like_article(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.like_article(user['user_id'], article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/dislike/{article_id}")
def dislike_article(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.dislike_article(user['user_id'], article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))