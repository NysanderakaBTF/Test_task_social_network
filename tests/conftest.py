import pytest

from core.db.db_config import Base, sync_engine


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


pytest_plugins = ('pytest_asyncio',)
