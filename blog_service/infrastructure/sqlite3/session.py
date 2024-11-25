from sqlmodel import SQLModel, Session, create_engine
from core.config import get_settings

settings = get_settings()

# SQLite database URL
SQLITE_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLITE_DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False}
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
