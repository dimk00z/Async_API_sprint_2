import asyncio
from uuid import UUID
from http import HTTPStatus

from pydantic import BaseModel
from models.person import PersonRole
from fastapi import Query, Depends, APIRouter, HTTPException
from services.person import PersonService, get_person_service

router = APIRouter()


class PersonFilm(BaseModel):
    uuid: UUID
    title: str
    role: PersonRole


class Person(BaseModel):
    uuid: UUID
    full_name: str
    films: list[PersonFilm] = []


@router.get("/search", response_model=list[Person], summary="Поиск по персонам")
async def person_search(
    query: str,
    page_number: int = Query(0, alias="page[number]"),
    page_size: int = Query(25, alias="page[size]"),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    """
    Для вывода доступны следующие параметры:
    - **query**: строка для поиска
    - **page[number]**: запрашиваемая страница
    - **page[size]**: размер страницы

    Check me: http://localhost:8000/api/v1/person/search?query=george&page[number]=0&page[size]=5
    """

    persons = await person_service.get_by_full_name(
        query_full_name=query, page_number=page_number, page_size=page_size
    )

    films_of_persons = await asyncio.gather(
        *[person_service.get_films_by_person_uuid(person.uuid) for person in persons]
    )
    for person, films in zip(persons, films_of_persons):
        person.films = films

    return [
        Person(uuid=person.uuid, full_name=person.full_name, films=person.films)
        for person in persons
    ]


@router.get("/{person_uuid}/film", summary="Вывод фильмов для персоны")
async def person_films(
    person_uuid: UUID,
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonFilm]:
    """
    Вывод информации о фильма для персоне по uuid:

    - **person_uuid**: требуемое поле

    Check me: http://localhost:8000/api/v1/person/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a/film
    """

    person = await person_service.get_by_uuid(person_uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    person_films = await person_service.get_films_by_person_uuid(person_uuid)

    return [PersonFilm(uuid=film.uuid, title=film.title, role=film.role) for film in person_films]


@router.get("/{person_uuid}", response_model=Person, summary="Подробная информация о персоне")
async def person_details(
    person_uuid: UUID, person_service: PersonService = Depends(get_person_service)
) -> Person:
    """
    Вывод информации о персоне по uuid:

    - **person_uuid**: требуемое поле

    Check me: http://localhost:8000/api/v1/person/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a
    """

    person = await person_service.get_by_uuid(person_uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    person_films = await person_service.get_films_by_person_uuid(person_uuid)

    return Person(uuid=person.uuid, full_name=person.full_name, films=person_films)
