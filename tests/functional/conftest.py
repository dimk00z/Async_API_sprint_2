import pytest
from settings import Settings
from utils.setup import redis_setup, elastic_setup
from utils.connections import redis_connect, elastic_connect


@pytest.fixture(scope="session")
def settings():
    return Settings()


@pytest.fixture(scope="session")
async def elastic_client(settings):
    """Установка соединения + настройка Elastic клиента."""
    client = await elastic_connect(host=settings.es_host)

    await elastic_setup(es_client=client)

    yield client
    await client.close()


@pytest.fixture(scope="session")
async def redis_client(settings):
    """Установка соединения + настройка Redis клиента."""
    client = await redis_connect(host=settings.redis_host, port=settings.redis_port)

    await redis_setup(redis_client=client)

    yield client
    await client.close()
