import json

from aioredis import Redis
from settings import ES_INDEXES_FILES
from elasticsearch._async import helpers
from elasticsearch import AsyncElasticsearch


async def elastic_setup(es_client: AsyncElasticsearch) -> None:
    """Удалить все индексы из эластика и заполнить их данными из файлов."""

    for es_index, file_path in ES_INDEXES_FILES:
        await es_client.indices.delete(index=es_index, ignore=[400, 404])

        with open(file_path) as f_in:
            docs = [json.loads(line) for line in f_in.readlines()]

        await helpers.async_bulk(es_client, docs)


async def redis_setup(redis_client: Redis) -> None:
    """Удалить все из редиса."""
    await redis_client.flushall()
