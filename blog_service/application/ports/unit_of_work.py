from typing import Protocol
from application.ports.repositories.post_repository import PostRepository
from application.ports.repositories.comment_repository import CommentRepository

class UnitOfWork(Protocol):
    posts: PostRepository
    comments: CommentRepository

    async def __aenter__(self) -> "UnitOfWork":
        """Start a new transaction"""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """End the transaction"""
        ...

    async def commit(self) -> None:
        """Commit the transaction"""
        ...

    async def rollback(self) -> None:
        """Rollback the transaction"""
        ...
