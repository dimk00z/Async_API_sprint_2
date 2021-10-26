import os
import sys
import asyncio
import inspect
import logging

import backoff
import aioredis
import settings
from elasticsearch import AsyncElasticsearch

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def backoff_handler(details):
    logging.error(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=settings.CONNECTIONS_MAX_TIME,
)
async def redis_connect(*, host: str, port: int) -> aioredis.Redis:
    redis = aioredis.from_url(f"redis://{host}:{port}")
    pong = await redis.ping()
    if not pong:
        raise ConnectionError("Connection failed")
    return redis


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=settings.CONNECTIONS_MAX_TIME,
)
async def elastic_connect(*, host: str) -> AsyncElasticsearch:
    elastic = AsyncElasticsearch(hosts=host, verify_certs=True)
    if not await elastic.ping():
        raise ConnectionError("Connection failed")
    return elastic


async def main():
    "Waiters for Elasticsearch and REDIS"
    await elastic_connect(host=settings.es_host)
    await redis_connect(host=settings.redis_host, port=settings.redis_port)


if __name__ == "__main__":
    asyncio.run(main())
