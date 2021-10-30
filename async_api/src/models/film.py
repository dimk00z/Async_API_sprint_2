from uuid import UUID

from pydantic import BaseModel
from pydantic.schema import Optional

from .genre import Genre
from .abstract_model import AbstractModel


class PersonForFilm(BaseModel):
    uuid: UUID
    full_name: str


class Film(AbstractModel):
    uuid: UUID
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genres: list[Genre]
    writers: list[PersonForFilm]
    actors: list[PersonForFilm]
    directors: list[PersonForFilm]
