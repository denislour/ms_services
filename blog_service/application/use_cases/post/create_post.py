from domain.entities.post import Post
from application.ports.repositories.post_repository import PostRepository

class CreatePost:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    async def execute(self, post: Post) -> Post:
        return await self.post_repository.create(post)
