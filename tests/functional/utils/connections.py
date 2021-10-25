import logging

import backoff
import aioredis
from settings import CONNECTIONS_MAX_TIME
from elasticsearch import AsyncElasticsearch


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
    max_time=CONNECTIONS_MAX_TIME,
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
    max_time=CONNECTIONS_MAX_TIME,
)
async def elastic_connect(*, host: str) -> AsyncElasticsearch:
    elastic = AsyncElasticsearch(hosts=host, verify_certs=True)
    if not await elastic.ping():
        raise ConnectionError("Connection failed")
    return elastic
