from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from server.controller.article_controller import ArticleController
from server.core.jwt_utils import get_current_user
from server.core.jwt_utils import admin_required
from server.schemas.report_article import ReportArticleRequest
from server.schemas.report_article import ReportArticleRequest
from server.Exceptions.report_exceptions import ReportNotFoundException

router = APIRouter(prefix="/report_article", tags=["report_article"])
controller = ArticleController()


@router.post("/report")
def report_article(request: ReportArticleRequest, user=Depends(get_current_user), reason: Optional[str] = None):
    try:
        return controller.report_article(request.article_id, user["user_id"], reason)
    except ReportNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/admin/reported-articles")
def get_reported_articles(user= Depends(admin_required)):
    try:
        return controller.get_reported_articles()
    except ReportNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.put("/admin/articles/{article_id}/hide")
def hide_article(article_id: int, user = Depends(admin_required)):
    try:
        return controller.hide_article(article_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.put("/admin/articles/{article_id}/unhide")
def unhide_article(article_id: int, user = Depends(admin_required)):
    try:
        return controller.unhide_article(article_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))