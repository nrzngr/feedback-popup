from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class FeedbackModel(BaseModel):
    id: int
    rating: int
    satisfaction: str
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class FeedbackCreateModel(BaseModel):
    rating: int
    description: str  # Make description optional

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "rating": "5",
                "description": "I'm really satisfied with this service!"
            }
        }
    )
