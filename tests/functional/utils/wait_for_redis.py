import asyncio
import logging

import backoff
import aioredis
import add_parent_path
from settings import TestSettings
from backoff_hdlr import backoff_hdlr

settings = TestSettings()


@backoff.on_exception(backoff.expo, (ConnectionError), on_backoff=backoff_hdlr)
async def wait_for_redis(host: str, port: str) -> None:
    redis = aioredis.from_url(f"redis://{host}:{port}")
    await redis.ping()


async def main():
    await wait_for_redis(host=settings.redis_host, port=settings.redis_port)


if __name__ == "__main__":
    asyncio.run(main())
    logging.info("Connected to Redis:%s", settings.redis_host)
