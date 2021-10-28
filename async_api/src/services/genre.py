from functools import lru_cache

from fastapi import Depends
from models.genre import Genre
from db.elastic import get_elastic
from services.base import MainService
from elasticsearch import AsyncElasticsearch


class GenreService(MainService):
    index = "genres"
    model = Genre

    async def genre_list(self,
                         page_number: int,
                         page_size: int,) -> list[Genre]:
        searched_genres = await self._search(query={"match_all": {}},
                                             from_=page_number * page_size if page_number > 1 else 0,
                                             size=page_size)
        return [self.model(**doc["_source"]) for doc in searched_genres]


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
