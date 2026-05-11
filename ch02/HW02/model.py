from pydantic import BaseModel, Field
from datetime import datetime


class LostItem(BaseModel):
    id: int
    item_name: str = Field(..., min_length=2, max_length=20)
    found_place: str = Field(..., min_length=2, max_length=30)
    found_time: datetime
    is_returned: bool = False