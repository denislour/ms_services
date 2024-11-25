from typing import List, Protocol
from uuid import UUID
from domain.entities.comment import Comment

class CommentRepository(Protocol):
    async def add(self, comment: Comment) -> Comment:
        """Add a new comment"""
        ...

    async def get(self, comment_id: UUID) -> Comment:
        """Get a comment by id"""
        ...

    async def get_by_post(self, post_id: UUID) -> List[Comment]:
        """Get all comments for a post"""
        ...

    async def update(self, comment: Comment) -> Comment:
        """Update a comment"""
        ...

    async def delete(self, comment_id: UUID) -> None:
        """Delete a comment"""
        ...

    async def delete_by_post(self, post_id: UUID) -> None:
        """Delete all comments for a post"""
        ...
