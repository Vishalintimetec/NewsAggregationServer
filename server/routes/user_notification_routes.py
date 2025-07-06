from fastapi import APIRouter, Depends, HTTPException
from server.schemas.notification import NotificationPreferenceCreate, NotificationPreferenceOut, \
     BulkNotificationConfig
from server.controller.user_notification_controller import NotificationController
from server.core.jwt_utils import get_current_user
from typing import List

router = APIRouter(prefix="/notifications", tags=["notifications"])
controller = NotificationController()

# @router.post("/preference")
# def create_preference(preference: NotificationPreferenceCreate, user=Depends(get_current_user)):
#     return controller.create_preference(user["user_id"], preference)

@router.get("/preferences", response_model=List[NotificationPreferenceOut])
def get_preferences(user=Depends(get_current_user)):
    return controller.get_preferences(user["user_id"])

@router.post("/configure-notifications")
def configure_notifications(config_data: BulkNotificationConfig, user=Depends(get_current_user)):
    return controller.configure_notifications(user["user_id"], config_data)

@router.delete("/preference/{preference_id}")
def delete_preference(preference_id: int, user=Depends(get_current_user)):
    return controller.delete_preference(user["user_id"], preference_id)
