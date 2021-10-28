from uuid import UUID
from http import HTTPStatus
from typing import Optional

from models.genre import Genre
from fastapi import Depends, APIRouter, HTTPException, Query
from services.genre import GenreService, get_genre_service

router = APIRouter()

genres = Optional[list[dict[str, str]]]


@router.get("/")
async def genre_list(
    genre_service: GenreService = Depends(get_genre_service),
    page_number: int = Query(1, alias="page[number]"),
    page_size: int = Query(50, alias="page[size]"),
) -> list[dict]:

    return await genre_list(
        genre_service=genre_service,
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
