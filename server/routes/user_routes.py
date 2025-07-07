from fastapi import APIRouter, Depends, Query, HTTPException
from server.controller.user_controller import UserController
from server.core.jwt_utils import get_current_user
from typing import Optional
from server.Exceptions.user_exceptions import UserNotFoundException, UserAlreadyExistsException, RepositoryException
from server.schemas.article_search import SearchArticleRequest

router = APIRouter(prefix="/user", tags=["user"])
controller = UserController()

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    try:
        return controller.get_current_user_info(user['user_id'])
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/headlines/today")
def get_today_headlines(user=Depends(get_current_user)):
    try:
        return controller.get_today_headlines(user['user_id'])
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/headlines/date-range")
def get_headlines_by_date_range(start_date: str = Query(...), end_date: str = Query(...), user=Depends(get_current_user), category: Optional[str] = None):
    try:
        return controller.get_headlines_by_date_range(user['user_id'], start_date, end_date, category)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/saved_articles")
def get_saved_articles(user=Depends(get_current_user)):
    try:
        return controller.get_saved_articles(user['user_id'])
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/save_article/{article_id}")
def save_article(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.save_article(user['user_id'], article_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.delete("/delete_article/{article_id}")
def delete_saved_article(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.delete_article(user['user_id'], article_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/search")
def search_articles(search_request: SearchArticleRequest, user=Depends(get_current_user)):
    try:
        return {"articles": controller.search_articles(search_request, user['user_id'])}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/logout")
def logout(user=Depends(get_current_user)):
    try:
        return controller.logout(user['user_id'])
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

