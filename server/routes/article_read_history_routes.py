from fastapi import APIRouter, Depends, HTTPException
from server.controller.article_read_history_controller import ArticleReadHistoryController
from server.core.jwt_utils import get_current_user
from server.Exceptions.article_exceptions import ArticleNotFoundException

router = APIRouter(prefix="/read-history", tags=["read-history"])
controller = ArticleReadHistoryController()

@router.post("/read/{article_id}")
def record_read(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.record_read(user['user_id'], article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/read-history")
def get_read_history(user=Depends(get_current_user)):
    try:
        return controller.get_read_history(user['user_id'])
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))