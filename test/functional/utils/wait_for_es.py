import asyncio
import logging

import backoff
import add_parent_path
from settings import TestSettings
from backoff_hdlr import backoff_hdlr
from elasticsearch import ConnectionError, AsyncElasticsearch

settings = TestSettings()


@backoff.on_exception(
    backoff.expo,
    ConnectionError,
    on_backoff=backoff_hdlr,
    max_time=settings.wait_time,
)
async def wait_for_elastic(es: AsyncElasticsearch) -> None:
    if not await es.ping():
        raise ConnectionError("Connection failed")
    await es.close()


async def main():
    es: AsyncElasticsearch = AsyncElasticsearch(settings.es_host, verify_certs=True)
    await wait_for_elastic(es=es)


if __name__ == "__main__":
    asyncio.run(main())
    logging.info("Connected to Elasticsearch:%s", settings.es_host)
