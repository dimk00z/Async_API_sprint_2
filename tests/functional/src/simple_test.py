import pytest
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

INDEX = "movies"
FILM_ID = "3d825f60-9fff-4dfe-b294-1a45fa1e115d"


@pytest.mark.asyncio
async def test_elastic(elastic_client: AsyncElasticsearch):
    """Получить фильм по id и проверить его title."""
    film = await elastic_client.get(index=INDEX, id=FILM_ID)
    assert film
    assert film["_source"]["title"] == "Star Wars: Episode IV - A New Hope"


@pytest.mark.asyncio
async def test_redis(redis_client: Redis):
    """Проверить что в Redis нет ключей + базовые операции с ним."""
    keys = await redis_client.keys()
    assert len(keys) == 0

    await redis_client.set(FILM_ID, "Star Wars: Episode IV - A New Hope")
    assert (
        await redis_client.get(FILM_ID)
    ).decode() == "Star Wars: Episode IV - A New Hope"
