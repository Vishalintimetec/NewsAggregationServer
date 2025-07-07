from fastapi import APIRouter, Depends, HTTPException
from server.schemas.category import CategoryCreate
from server.controller.category_controller import CategoryController
from server.core.jwt_utils import admin_required
from server.schemas.category_visibility import CategoryVisibilityUpdate
from server.Exceptions.category_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException

controller = CategoryController()
router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/")
def add_category(category: CategoryCreate, user= Depends(admin_required)):
    try:
        return controller.create_category(category)
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.put("/admin/category/{category_id}/visibility")
def toggle_category_visibility(category_id: int, body: CategoryVisibilityUpdate,  user= Depends(admin_required)):
    try:
        return controller.toggle_category_visibility(category_id, body.is_visible)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/all")
def get_all_categories():
    try:
        return controller.get_all_categories()
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))