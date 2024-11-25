from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from domain.entities.comment import Comment

class CommentModel(SQLModel, table=True):
    __tablename__ = "comments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="posts.id")
    content: str
    author: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    @classmethod
    def from_entity(cls, comment: Comment) -> "CommentModel":
        return cls(
            id=comment.id,
            post_id=comment.post_id,
            content=comment.content,
            author=comment.author,
            created_at=comment.created_at,
            updated_at=comment.updated_at
        )

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            post_id=self.post_id,
            content=self.content,
            author=self.author,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def update_from_entity(self, comment: Comment) -> None:
        self.content = comment.content
        self.author = comment.author
        self.updated_at = datetime.utcnow()
