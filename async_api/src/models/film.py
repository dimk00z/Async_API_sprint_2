from uuid import UUID

from pydantic import BaseModel
from pydantic.schema import Optional

from .abstract_model import AbstractModel
from .genre import Genre


class PersonForFilm(BaseModel):
    uuid: UUID
    full_name: str


class Film(AbstractModel):
    uuid: UUID
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    genres: list[Genre]
    writers: Optional[list[PersonForFilm]]
    actors: Optional[list[PersonForFilm]]
    directors: Optional[list[PersonForFilm]]
