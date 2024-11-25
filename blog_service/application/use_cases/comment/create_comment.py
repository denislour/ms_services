from uuid import uuid4, UUID
from datetime import datetime
from domain.entities.comment import Comment
from application.ports.unit_of_work import UnitOfWork

class CreateComment:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(
        self,
        post_id: UUID,
        content: str,
        author: str
    ) -> Comment:
        comment = Comment(
            id=uuid4(),
            post_id=post_id,
            content=content,
            author=author,
            created_at=datetime.utcnow()
        )

        async with self.uow as uow:
            # Verify post exists
            post = await uow.posts.get(post_id)
            if not post:
                raise ValueError(f"Post {post_id} not found")

            # Create comment
            created_comment = await uow.comments.add(comment)
            await uow.commit()
            return created_comment
