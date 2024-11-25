from typing import Optional
from blog_service.app.domain.entities.post import Post
from blog_service.app.domain.ports.post_repository import PostRepository
from blog_service.app.domain.value_objects.post_status import PostStatus

class ChangePostStatus:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    async def execute(self, post_id: int, status: PostStatus) -> Optional[Post]:
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            return None
        
        post.status = status
        return await self.post_repository.update(post_id, post)
