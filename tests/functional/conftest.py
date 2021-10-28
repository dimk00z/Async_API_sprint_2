import asyncio
from dataclasses import dataclass

import pytest
import aiohttp
from settings import Settings
from multidict import CIMultiDictProxy
from utils.setup import redis_setup, elastic_setup
from utils.connections import redis_connect, elastic_connect


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def settings():
    return Settings()


@pytest.fixture(scope="session", autouse=True)
async def elastic_client(settings):
    """Установка соединения + настройка Elastic клиента."""
    client = await elastic_connect(host=settings.es_host)

    await elastic_setup(es_client=client)

    yield client
    await client.close()


@pytest.fixture(scope="session", autouse=True)
async def redis_client(settings):
    """Установка соединения + настройка Redis клиента."""
    client = await redis_connect(host=settings.redis_host, port=settings.redis_port)

    await redis_setup(redis_client=client)

    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def get_request(session, settings):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        async_api_host = settings.async_api_host
        # export ASYNC_API_HOST="http://178.154.213.182:8000/api/v1" - для проверки на живом
        # python -m pytest -vv
        url = f"{async_api_host}{method}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
