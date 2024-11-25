from typing import Callable, Any
from functools import lru_cache
from sqlmodel import Session
from motor.motor_asyncio import AsyncIOMotorDatabase

from application.ports.repositories.post_repository import PostRepository
from infrastructure.sqlite3.repositories.post_repository import SQLitePostRepository
from infrastructure.mongodb.repositories.post_repository import MongoPostRepository
from infrastructure.sqlite3.session import get_session as get_sqlite_session
from infrastructure.mongodb.session import get_database as get_mongo_db

class DBFactory:
    """Factory for creating database dependencies"""
    
    _db_type: str = "sqlite"  # default database type
    
    @classmethod
    def set_db_type(cls, db_type: str):
        """Set the database type to use"""
        cls._db_type = db_type.lower()
    
    @classmethod
    @lru_cache
    def get_repository_factory(cls) -> Callable[..., PostRepository]:
        """Get the appropriate repository factory based on database type"""
        if cls._db_type == "sqlite":
            def get_repository(session: Session = get_sqlite_session()) -> PostRepository:
                return SQLitePostRepository(session)
            return get_repository
        elif cls._db_type == "mongo":
            async def get_repository(db: AsyncIOMotorDatabase = get_mongo_db()) -> PostRepository:
                return MongoPostRepository(db)
            return get_repository
        else:
            raise ValueError(f"Unsupported database type: {cls._db_type}")
    
    @classmethod
    def get_session_factory(cls) -> Callable[..., Any]:
        """Get the appropriate session factory based on database type"""
        if cls._db_type == "sqlite":
            return get_sqlite_session
        elif cls._db_type == "mongo":
            return get_mongo_db
        else:
            raise ValueError(f"Unsupported database type: {cls._db_type}")
