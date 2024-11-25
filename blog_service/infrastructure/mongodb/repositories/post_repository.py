from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from domain.entities.post import Post
from ..models.post import PostDocument

class MongoPostRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def add(self, post: Post) -> Post:
        doc = PostDocument.to_document(post)
        await self.collection.insert_one(doc)
        return post

    async def get(self, post_id: UUID) -> Optional[Post]:
        doc = await self.collection.find_one({"_id": str(post_id)})
        return PostDocument.from_document(doc) if doc else None

    async def update(self, post: Post) -> Optional[Post]:
        doc = PostDocument.to_document(post)
        result = await self.collection.replace_one(
            {"_id": str(post.id)},
            doc
        )
        return post if result.modified_count > 0 else None

    async def delete(self, post_id: UUID) -> None:
        await self.collection.delete_one({"_id": str(post_id)})

    async def list(self) -> List[Post]:
        cursor = self.collection.find()
        docs = await cursor.to_list(length=None)
        return [PostDocument.from_document(doc) for doc in docs]
