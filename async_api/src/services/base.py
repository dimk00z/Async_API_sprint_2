import hashlib
import logging
from uuid import UUID

from aiocache import cached
from pydantic import BaseModel
from db.redis import get_redis_cache_config
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import RequestError, NotFoundError

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class MainService:
    # Определяем базовую модель и индекс, будет указываться при добавлении модели жанра
    model = BaseModel
    index = ""

    # Инициализация класса, определение настроек redis и elastic
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    def key_builder(self, *args, **kwargs):
        "Генерация хэш ключа для кэша по kwargs"

        args_line: str = str(sorted(kwargs.items()))
        cache_key = hashlib.md5(args_line.encode()).hexdigest()
        return cache_key

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_config(),
        key_builder=key_builder,
    )
    async def get_by_uuid(self, uuid: UUID):
        result_object = {}
        try:
            doc_ = await self.elastic.get(index=self.index, id=str(uuid))
            result_object = self.model(**doc_["_source"])

        except (RequestError, NotFoundError) as elastic_error:
            logging.error(elastic_error)
        finally:
            return result_object

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_config(),
        key_builder=key_builder,
    )
    async def _search(self, index: str = None, **search_options):
        index = index or self.index
        result_objects = []
        try:
            response = await self.elastic.search(index=index, **search_options)
            if response:
                result_objects = response["hits"]["hits"]
        except (RequestError, NotFoundError) as elastic_error:
            logging.error(elastic_error)
        finally:
            return result_objects
