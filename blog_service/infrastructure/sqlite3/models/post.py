from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from domain.entities.post import Post
from domain.value_objects.post_status import PostStatus
from .comment import CommentModel

class PostModel(SQLModel, table=True):
    __tablename__ = "posts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    content: str
    author: str = Field(index=True)
    status: PostStatus = Field(default=PostStatus.DRAFT)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationships
    comments: List["CommentModel"] = Relationship(
        back_populates="post",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )

    @classmethod
    def from_entity(cls, post: Post) -> "PostModel":
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            author=post.author,
            status=post.status,
            created_at=post.created_at,
            updated_at=post.updated_at
        )

    def to_entity(self) -> Post:
        return Post(
            id=self.id,
            title=self.title,
            content=self.content,
            author=self.author,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            comments=[comment.to_entity() for comment in self.comments]
        )

    def update_from_entity(self, post: Post) -> None:
        self.title = post.title
        self.content = post.content
        self.author = post.author
        self.status = post.status
        self.updated_at = datetime.utcnow()
