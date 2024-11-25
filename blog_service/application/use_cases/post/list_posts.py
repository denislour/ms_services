from typing import List
from blog_service.app.domain.entities.post import Post
from blog_service.app.domain.ports.post_repository import PostRepository

class ListPosts:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    async def execute(self) -> List[Post]:
        return await self.post_repository.get_all()
