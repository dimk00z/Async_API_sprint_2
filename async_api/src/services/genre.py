from functools import lru_cache

from fastapi import Depends
from models.genre import Genre
from db.elastic import get_elastic
from services.base import MainService
from elasticsearch import AsyncElasticsearch


class GenreService(MainService):
    index = "genres"
    model = Genre

    async def get_genres(
        self,
        **end_point_params,
    ) -> list[Genre]:
        searched_genres = await self._search(**self._parse_params(**end_point_params))
        return [self.model(**doc["_source"]) for doc in searched_genres]


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
