from uuid import UUID
from http import HTTPStatus
from typing import Optional

from models.genre import Genre
from fastapi import Depends, APIRouter, HTTPException, Query
from services.genre import GenreService, get_genre_service

router = APIRouter()

genres = Optional[list[dict[str, str]]]


async def get_genres(
        genres_service: GenreService = Depends(get_genre_service),
        page_number: int = 1,
        page_size: int = 50
):
    genres = await genres_service.get_genres(
        page_number=page_number,
        page_size=page_size,
    )
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="not one genre found"
        )


@router.get("/")
async def genres_list(
        genres_service: GenreService = Depends(get_genre_service),
        page_number: int = Query(1, alias="page[number]"),
        page_size: int = Query(50, alias="page[size]"),
) -> list[dict]:
    return await get_genres(
        genres_service=genres_service,
        page_number=page_number,
        page_size=page_size,
    )


@router.get("/{genre_uuid}")
async def genre_details(
        genre_uuid: UUID,
        genre_service: GenreService = Depends(get_genre_service),
) -> Optional[Genre]:
    genre = await genre_service.get_by_uuid(uuid=genre_uuid)
    if genre:
        return genre
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
