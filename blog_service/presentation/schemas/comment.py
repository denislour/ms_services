from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    author: str = Field(..., min_length=1, max_length=100)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "content": "Great post! Thanks for sharing.",
                "author": "Jane Doe"
            }
        }
    )

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "content": "Updated comment content"
            }
        }
    )

class CommentResponse(CommentBase):
    id: UUID
    post_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "post_id": "123e4567-e89b-12d3-a456-426614174001",
                "content": "This is a comment",
                "author": "Jane Doe",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00"
            }
        }
    )
