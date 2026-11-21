import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    asyncio.run(init_db())

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
