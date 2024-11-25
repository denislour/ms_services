from typing import Optional
from blog_service.app.domain.entities.post import Post
from blog_service.app.domain.ports.post_repository import PostRepository

class GetPost:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    async def execute(self, post_id: int) -> Optional[Post]:
        return await self.post_repository.get_by_id(post_id)
