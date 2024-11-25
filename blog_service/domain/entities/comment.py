from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class Comment(BaseModel):
    id: UUID
    post_id: UUID
    content: str = Field(min_length=1)
    author: str = Field(min_length=1)
    created_at: datetime
    updated_at: Optional[datetime] = None

    def can_edit(self, user_id: UUID) -> bool:
        return self.author == user_id

    class Config:
        frozen = True  # Immutable
