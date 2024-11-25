from infrastructure.sqlite3.session import Session
from infrastructure.sqlite3.repositories.post_repository import SQLitePostRepository
from infrastructure.sqlite3.repositories.comment_repository import SQLiteCommentRepository

class SQLiteUnitOfWork:
    def __init__(self):
        self._session: Session | None = None
        self.posts: SQLitePostRepository | None = None
        self.comments: SQLiteCommentRepository | None = None

    async def __aenter__(self) -> "SQLiteUnitOfWork":
        self._session = Session()
        self.posts = SQLitePostRepository(self._session)
        self.comments = SQLiteCommentRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        await self._session.close()
        self._session = None
        self.posts = None
        self.comments = None

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
