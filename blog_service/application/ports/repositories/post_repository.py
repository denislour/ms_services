from typing import Protocol, List, Optional
from domain.entities.post import Post

class PostRepository(Protocol):
    """Repository interface for post persistence"""
    
    async def create(self, post: Post) -> Post:
        """Create a new post"""
        ...

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        """Get a post by ID"""
        ...

    async def get_all(self) -> List[Post]:
        """Get all posts"""
        ...

    async def update(self, post_id: int, post: Post) -> Optional[Post]:
        """Update a post"""
        ...

    async def delete(self, post_id: int) -> bool:
        """Delete a post"""
        ...
