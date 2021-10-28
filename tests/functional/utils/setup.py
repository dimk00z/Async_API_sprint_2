import json

from aioredis import Redis
from elasticsearch._async import helpers
from elasticsearch import AsyncElasticsearch
from settings import ES_SCHEMA_FILE, ES_INDEXES_FILES


async def elastic_setup(es_client: AsyncElasticsearch) -> None:
    """Удалить все индексы из эластика и заполнить их данными из файлов."""

    with open(ES_SCHEMA_FILE) as f_in:
        schema = json.load(f_in)

    for es_index, file_path in ES_INDEXES_FILES:
        await es_client.indices.delete(index=es_index, ignore=[400, 404])
        await es_client.indices.create(
            index=es_index, ignore=400, body=schema[es_index]
        )
        with open(file_path) as f_in:
            docs = [json.loads(line) for line in f_in.readlines()]

        await helpers.async_bulk(es_client, docs)


async def redis_setup(redis_client: Redis) -> None:
    """Удалить все из редиса."""
    redis_client.flushdb(async_op=False)
