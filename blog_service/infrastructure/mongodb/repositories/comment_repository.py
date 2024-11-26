from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from domain.entities.comment import Comment
from application.ports.repositories.comment_repository import CommentRepository
from ..models.comment import CommentDocument

class MongoCommentRepository(CommentRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def add(self, comment: Comment) -> Comment:
        doc = CommentDocument.to_document(comment)
        await self.collection.insert_one(doc)
        return comment

    async def get(self, comment_id: UUID) -> Optional[Comment]:
        doc = await self.collection.find_one({"_id": str(comment_id)})
        return CommentDocument.from_document(doc) if doc else None

    async def get_by_post(self, post_id: UUID) -> List[Comment]:
        cursor = self.collection.find({"post_id": str(post_id)})
        docs = await cursor.to_list(length=None)
        return [CommentDocument.from_document(doc) for doc in docs]

    async def update(self, comment: Comment) -> Optional[Comment]:
        doc = CommentDocument.to_document(comment)
        result = await self.collection.replace_one(
            {"_id": str(comment.id)},
            doc
        )
        return comment if result.modified_count > 0 else None

    async def delete(self, comment_id: UUID) -> None:
        await self.collection.delete_one({"_id": str(comment_id)})

    async def delete_by_post(self, post_id: UUID) -> None:
        await self.collection.delete_many({"post_id": str(post_id)})
