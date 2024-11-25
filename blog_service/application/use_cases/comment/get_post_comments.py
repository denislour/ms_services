from typing import List
from uuid import UUID
from domain.entities.comment import Comment
from application.ports.unit_of_work import UnitOfWork

class GetPostComments:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, post_id: UUID) -> List[Comment]:
        async with self.uow as uow:
            return await uow.comments.get_by_post(post_id)
