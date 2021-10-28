from uuid import UUID
from http import HTTPStatus
from typing import Optional

from models.film import Film
from services.film import FilmService, get_film_service
from fastapi import Query, Depends, APIRouter, HTTPException

router = APIRouter()

persons = Optional[list[dict[str, str]]]


async def get_films(
    film_service: FilmService = Depends(get_film_service),
    filter_genre: Optional[str] = "",
    sort: Optional[str] = Query(None, regex="^-?[a-zA-Z_]+$"),
    page_number: int = 1,
    page_size: int = 50,
    query: Optional[str] = "",
):
    films = await film_service.get_films(
        sort=sort,
        filter_genre=filter_genre if filter_genre is not Query(None) else "",
        page_number=page_number,
        page_size=page_size,
        query=str(query),
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="not one film found")
    if "error" in films:
        return HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=films["error"])
    return [
        {
            "uuid": film.uuid,
            "title": film.title,
            "imdb_rating": film.imdb_rating,
        }
        for film in films
    ]


@router.get(
    "/",
    summary="Список кинопроизведений",
)
async def films_list(
    film_service: FilmService = Depends(get_film_service),
    filter_genre: Optional[str] = Query(None, alias="filter[genre]"),
    sort_: Optional[str] = Query(None, regex="^-?[a-zA-Z_]+$", alias="sort"),
    page_number: int = Query(1, alias="page[number]"),
    page_size: int = Query(50, alias="page[size]"),
) -> list[dict]:
    """
    Для вывода доступны следующие параметры:
    - **filter[genre]**: сортировка по uuid жанра"
    - **sort**: сортировка по рейтингу -imdb_rating/imdb_rating
    - **page[number]**: запрашиваемая страница
    - **page[size]**: размер страницы

    """
    return await get_films(
        film_service=film_service,
        sort=sort_,
        filter_genre=filter_genre,
        page_number=page_number,
        page_size=page_size,
    )


@router.get(
    "/search",
    summary="Поиск кинопроизведений",
)
async def films_search(
    film_service: FilmService = Depends(get_film_service),
    sort_: Optional[str] = Query(None, regex="^-?[a-zA-Z_]+$", alias="sort"),
    page_number_: int = Query(1, alias="page[number]"),
    page_size_: int = Query(50, alias="page[size]"),
    query_: Optional[str] = Query(
        None,
        alias="query",
    ),
) -> list[dict]:
    """
    Для поиска доступны следующие параметры:
    - **query**: строка для поиска
    - **sort**: сортировка по рейтингу -imdb_rating/imdb_rating
    - **page[number]**: запрашиваемая страница
    - **page[size]**: размер страницы
    """
    return await get_films(
        film_service=film_service,
        sort=sort_,
        query=query_,
        page_number=page_number_,
        page_size=page_size_,
    )


@router.get(
    "/{film_uuid}",
    response_model=Film,
    summary="Подробные данные о фильме",
)
async def film_details(
    film_uuid: UUID,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    """
    Вывод информации о фильме по uuid:

    - **film_uuid**: требуемое поле
    """
    film = await film_service.get_by_uuid(uuid=film_uuid)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Film.parse_obj(film)
