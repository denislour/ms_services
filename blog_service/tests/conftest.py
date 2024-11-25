import pytest
from typing import AsyncGenerator
from uuid import UUID, uuid4
from domain.entities.post import Post
from domain.entities.comment import Comment
from domain.value_objects.post_status import PostStatus

class MockRepository:
    def __init__(self):
        self.items = {}

    async def add(self, item):
        self.items[str(item.id)] = item
        return item

    async def get(self, id: UUID):
        return self.items.get(str(id))

    async def list(self):
        return list(self.items.values())

    async def update(self, item):
        if str(item.id) in self.items:
            self.items[str(item.id)] = item
            return item
        return None

    async def delete(self, id: UUID):
        self.items.pop(str(id), None)

class MockUnitOfWork:
    def __init__(self):
        self.posts = MockRepository()
        self.comments = MockRepository()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

@pytest.fixture
async def uow() -> AsyncGenerator[MockUnitOfWork, None]:
    yield MockUnitOfWork()

@pytest.fixture
def sample_post() -> Post:
    return Post(
        id=uuid4(),
        title="Test Post",
        content="Test Content",
        author="Test Author",
        status=PostStatus.DRAFT
    )

@pytest.fixture
def sample_comment(sample_post) -> Comment:
    return Comment(
        id=uuid4(),
        post_id=sample_post.id,
        content="Test Comment",
        author="Test Commenter"
    )
