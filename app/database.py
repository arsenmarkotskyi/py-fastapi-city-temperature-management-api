from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# URL for async SQLite (requires aiosqlite)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./cities.db"

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  # Output SQL queries to console (for development)
)

# Create session factory for async operations
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass


# Dependency injection for getting database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session