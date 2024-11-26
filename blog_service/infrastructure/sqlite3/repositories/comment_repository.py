from typing import List
from uuid import UUID
from sqlmodel import select
from domain.entities.comment import Comment
from application.ports.repositories.comment_repository import CommentRepository
from infrastructure.sqlite3.models.comment import CommentModel
from infrastructure.sqlite3.session import Session

class SQLiteCommentRepository(CommentRepository):
    def __init__(self, session: Session):
        self.session = session

    async def add(self, comment: Comment) -> Comment:
        comment_model = CommentModel.from_entity(comment)
        self.session.add(comment_model)
        await self.session.flush()
        return comment_model.to_entity()

    async def get(self, comment_id: UUID) -> Comment:
        stmt = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self.session.execute(stmt)
        comment_model = result.scalar_one_or_none()
        return comment_model.to_entity() if comment_model else None

    async def get_by_post(self, post_id: UUID) -> List[Comment]:
        stmt = select(CommentModel).where(CommentModel.post_id == post_id)
        result = await self.session.execute(stmt)
        comment_models = result.scalars().all()
        return [cm.to_entity() for cm in comment_models]

    async def update(self, comment: Comment) -> Comment:
        stmt = select(CommentModel).where(CommentModel.id == comment.id)
        result = await self.session.execute(stmt)
        comment_model = result.scalar_one_or_none()
        if comment_model:
            comment_model.content = comment.content
            comment_model.author = comment.author
            comment_model.updated_at = comment.updated_at
            await self.session.flush()
            return comment_model.to_entity()
        return None

    async def delete(self, comment_id: UUID) -> None:
        stmt = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self.session.execute(stmt)
        comment_model = result.scalar_one_or_none()
        if comment_model:
            await self.session.delete(comment_model)
            await self.session.flush()

    async def delete_by_post(self, post_id: UUID) -> None:
        stmt = select(CommentModel).where(CommentModel.post_id == post_id)
        result = await self.session.execute(stmt)
        comment_models = result.scalars().all()
        for comment_model in comment_models:
            await self.session.delete(comment_model)
        await self.session.flush()

    async def list(self) -> List[Comment]:
        stmt = select(CommentModel)
        result = await self.session.execute(stmt)
        comment_models = result.scalars().all()
        return [cm.to_entity() for cm in comment_models]
