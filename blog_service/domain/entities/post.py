from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from domain.value_objects.post_status import PostStatus
from .comment import Comment

class Post(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str
    status: PostStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[Comment] = Field(default_factory=list)

    def add_comment(self, comment: Comment) -> None:
        if comment.post_id != self.id:
            raise ValueError("Comment belongs to different post")
        self.comments.append(comment)

    def remove_comment(self, comment_id: UUID) -> None:
        self.comments = [c for c in self.comments if c.id != comment_id]

    def update_content(self, new_content: str) -> None:
        if not new_content:
            raise ValueError("Content cannot be empty")
        self.content = new_content
        self.updated_at = datetime.utcnow()

    model_config = {
        "frozen": True  # Immutable
    }
