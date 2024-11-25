from app.domain.ports.post_repository import PostRepository
from app.application.ports.use_cases.post_use_cases import DeletePostUseCase

class DeletePost(DeletePostUseCase):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    async def execute(self, post_id: int) -> bool:
        return await self.post_repository.delete(post_id)
