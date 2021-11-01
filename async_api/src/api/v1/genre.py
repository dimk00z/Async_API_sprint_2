from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()

genres = Optional[list[dict[str, str]]]


async def get_genres(
    genres_service: GenreService = Depends(get_genre_service),
    page_number: int = 0,
    page_size: int = 50,
):
    genres = await genres_service.get_genres(
        page_number=page_number,
        page_size=page_size,
    )
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="not one genre found"
        )
    return genres


@router.get("/", summary="Список жанров")
async def genres_list(
    genres_service: GenreService = Depends(get_genre_service),
    page_number: int = Query(1, alias="page[number]"),
    page_size: int = Query(50, alias="page[size]"),
) -> list[Genre]:
    """
    Возможно задать следующие параметры:
    - **page[number]**: запрашиваемая страница
    - **page[size]**: размер страницы
    """
    return await get_genres(
        genres_service=genres_service,
        page_number=page_number - 1,
        page_size=page_size,
    )


@router.get("/{genre_uuid}", summary="Поиск жанра по uuid")
async def genre_details(
    genre_uuid: UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> Optional[Genre]:
    """
    Обязательный параметр:
    - **genre_uuid**: uuid жанра
    """
    genre = await genre_service.get_by_uuid(uuid=genre_uuid)
    if genre:
        return genre
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
