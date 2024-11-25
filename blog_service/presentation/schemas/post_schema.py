from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from domain.value_objects.post_status import PostStatus

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=100)
    status: PostStatus = Field(default=PostStatus.DRAFT)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my blog post",
                "author": "John Doe",
                "status": "DRAFT"
            }
        }

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[PostStatus] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "content": "Updated content",
                "status": "PUBLISHED"
            }
        }

class PostResponse(PostBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments_count: int = Field(default=0, ge=0)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My Blog Post",
                "content": "Content of the post",
                "author": "John Doe",
                "status": "PUBLISHED",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
                "comments_count": 5
            }
        }
