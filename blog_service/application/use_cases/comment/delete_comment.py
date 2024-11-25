from uuid import UUID
from application.ports.unit_of_work import UnitOfWork

class DeleteComment:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, comment_id: UUID) -> None:
        async with self.uow as uow:
            # Delete comment
            await uow.comments.delete(comment_id)
            await uow.commit()
