import motor.motor_asyncio
from core.config import get_settings

settings = get_settings()

# MongoDB connection URL
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "blog_db"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

async def init_db():
    """Initialize MongoDB collections and indexes"""
    # Create indexes if needed
    await database.posts.create_index("title")
    await database.posts.create_index("author")

async def get_database():
    yield database

def get_collection(collection_name: str):
    return database[collection_name]
