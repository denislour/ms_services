from typing import Protocol, List, Optional
from app.domain.entities.post import Post
from app.domain.value_objects.post_status import PostStatus

class CreatePostUseCase(Protocol):
    async def execute(self, post: Post) -> Post:
        """Create a new blog post"""
        ...

class GetPostUseCase(Protocol):
    async def execute(self, post_id: int) -> Optional[Post]:
        """Get a blog post by ID"""
        ...

class ListPostsUseCase(Protocol):
    async def execute(self) -> List[Post]:
        """Get all blog posts"""
        ...

class UpdatePostUseCase(Protocol):
    async def execute(self, post_id: int, post: Post) -> Optional[Post]:
        """Update a blog post"""
        ...

class DeletePostUseCase(Protocol):
    async def execute(self, post_id: int) -> bool:
        """Delete a blog post"""
        ...

class ChangePostStatusUseCase(Protocol):
    async def execute(self, post_id: int, status: PostStatus) -> Optional[Post]:
        """Change post status"""
        ...
