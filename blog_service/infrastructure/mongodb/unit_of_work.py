from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from infrastructure.mongodb.repositories.post_repository import MongoPostRepository
from infrastructure.mongodb.repositories.comment_repository import MongoCommentRepository

class MongoUnitOfWork:
    def __init__(self, client: AsyncIOMotorClient, database_name: str):
        self._client = client
        self._db: AsyncIOMotorDatabase = client[database_name]
        self.posts: MongoPostRepository | None = None
        self.comments: MongoCommentRepository | None = None
        self._transaction = None

    async def __aenter__(self) -> "MongoUnitOfWork":
        # Start transaction
        self._transaction = await self._client.start_session()
        await self._transaction.start_transaction()

        # Initialize repositories with collections
        self.posts = MongoPostRepository(self._db.posts)
        self.comments = MongoCommentRepository(self._db.comments)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self._transaction.end_session()
            self._transaction = None
            self.posts = None
            self.comments = None

    async def commit(self) -> None:
        if self._transaction:
            await self._transaction.commit_transaction()

    async def rollback(self) -> None:
        if self._transaction:
            await self._transaction.abort_transaction()
