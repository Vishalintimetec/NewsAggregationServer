from typing import Optional
from fastapi import APIRouter, Depends
from server.controller.article_controller import ArticleController
from server.core.jwt_utils import get_current_user
from server.core.jwt_utils import admin_required
from server.schemas.report_article import ReportArticleRequest

router = APIRouter(prefix="/report_article", tags=["report_article"])
controller = ArticleController()


@router.post("/report")
def report_article(request: ReportArticleRequest, user=Depends(get_current_user), reason: Optional[str] = None):
    return controller.report_article(request.article_id, user["user_id"], reason)

@router.get("/admin/reported-articles")
def get_reported_articles(user= Depends(admin_required)):
    return controller.get_reported_articles()

@router.put("/admin/articles/{article_id}/hide")
def hide_article(article_id: int, user = Depends(admin_required)):
    return controller.hide_article(article_id)

@router.put("/admin/articles/{article_id}/unhide")
def unhide_article(article_id: int, user = Depends(admin_required)):
    return controller.unhide_article(article_id)
