from pydantic import BaseModel
from typing import Optional, List

class NotificationPreferenceCreate(BaseModel):
    category: str
    keyword: Optional[str]

class NotificationConfigItem(BaseModel):
    category_name: str
    category_id: int
    is_enabled: bool
    keywords: List[str]


class BulkNotificationConfig(BaseModel):
    configurations: List[NotificationConfigItem]

class NotificationPreferenceOut(NotificationPreferenceCreate):
    id: int
    user_id: int
