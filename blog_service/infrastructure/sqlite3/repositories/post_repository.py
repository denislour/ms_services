from typing import List, Optional
from sqlmodel import Session, select
from domain.entities.post import Post
from application.ports.repositories.post_repository import PostRepository

class SQLitePostRepository(PostRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create(self, post: Post) -> Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        return self.session.get(Post, post_id)

    async def get_all(self) -> List[Post]:
        statement = select(Post)
        return self.session.exec(statement).all()

    async def update(self, post_id: int, post: Post) -> Optional[Post]:
        db_post = await self.get_by_id(post_id)
        if not db_post:
            return None
        
        post_data = post.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(db_post, key, value)
        
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post

    async def delete(self, post_id: int) -> bool:
        post = await self.get_by_id(post_id)
        if not post:
            return False
        
        self.session.delete(post)
        self.session.commit()
        return True
