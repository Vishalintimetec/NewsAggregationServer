from fastapi import APIRouter, Depends, Query
from server.controller.user_controller import UserController
from server.core.jwt_utils import get_current_user
from typing import Optional

router = APIRouter(prefix="/user", tags=["user"])
controller = UserController()

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return controller.get_current_user_info(user['user_id'])

@router.get("/headlines/today")
def get_today_headlines(user=Depends(get_current_user)):
    return controller.get_today_headlines(user['user_id'])

@router.get("/headlines/date-range")
def get_headlines_by_date_range(start_date: str = Query(...), end_date: str = Query(...),
user=Depends(get_current_user), category: Optional[str] = None):
    return controller.get_headlines_by_date_range(user['user_id'],start_date, end_date, category)

@router.get("/saved_articles")
def get_saved_articles(user=Depends(get_current_user)):
    return controller.get_saved_articles(user['user_id'])

@router.post("/save_article/{article_id}")
def save_article(article_id: int, user=Depends(get_current_user)):
    return controller.save_article(user['user_id'], article_id)

@router.delete("/delete_article/{article_id}")
def delete_saved_article(article_id: int, user=Depends(get_current_user)):
    return controller.delete_article(user['user_id'], article_id)

@router.get("/search")
def search_articles(query: str, start_date: Optional[str] = None, end_date: Optional[str] = None, sort_by: Optional[str] = "likes"):
    return controller.search_articles(query, start_date, end_date, sort_by)

@router.post("/logout")
def logout(user=Depends(get_current_user)):
    return controller.logout(user['user_id'])

