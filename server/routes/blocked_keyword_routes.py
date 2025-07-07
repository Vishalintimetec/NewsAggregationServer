from fastapi import APIRouter, Depends, Query, HTTPException
from server.controller.blocked_keyword_controller import BlockedKeywordController
from server.core.jwt_utils import admin_required
from server.schemas.keyword_block_unblock import KeywordRequest
from server.Exceptions.blocked_keyword_exceptions import BlockedKeywordNotFoundException

router = APIRouter(prefix="/admin/keywords", tags=["admin-keywords"])
controller = BlockedKeywordController()

@router.post("/block")
def block_keyword(request: KeywordRequest, user=Depends(admin_required)):
    try:
        return controller.block_keyword(request.keyword)
    except BlockedKeywordNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/unblock")
def unblock_keyword(request: KeywordRequest, user=Depends(admin_required)):
    try:
        return controller.unblock_keyword(request.keyword)
    except BlockedKeywordNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/")
def list_blocked_keywords(user=Depends(admin_required)):
    try:
        return controller.get_all_keywords()
    except BlockedKeywordNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))