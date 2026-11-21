from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

# SQLite compatibility for async
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite:///"):
    db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(
    db_url,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        # Create all tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
