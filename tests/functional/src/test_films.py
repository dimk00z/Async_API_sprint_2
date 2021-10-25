import asyncio
from dataclasses import dataclass

import pytest
import aiohttp
from multidict import CIMultiDictProxy

SERVICE_URL = "http://178.154.213.182:8000"


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"{SERVICE_URL}/api/v1{method}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


film_id_params = [
    ("2a090dde-f688-46fe-a9f4-b781a985275e", "Star Wars: Knights of the Old Republic", 9.6, 200),
    ("fd78a0e5-d4ec-435e-8994-4ccbdfc4e60b", "Lone Star Restoration", 8.7, 200),
    ("3f8873be-f6b1-4f3f-8a01-873924659851", "Justin Bieber: A Star Was Born", 1, 200),
    ("3f8873be-f6b1-4f3f-8000-873924659851", None, None, 404),
]


@pytest.mark.parametrize("film_uuid, title, imdb_rating, expected_response_status", film_id_params)
@pytest.mark.asyncio
async def test_film_by_id(get_request, film_uuid, title, imdb_rating, expected_response_status):
    response = await get_request(f"/film/{film_uuid}")
    assert response.status == expected_response_status
    assert response.body.get("title", None) == title
    assert response.body.get("imdb_rating", None) == imdb_rating


films_sorting_params = ["imdb_rating", "-imdb_rating", "wrong_sort"]


@pytest.mark.parametrize("sorting", films_sorting_params)
@pytest.mark.asyncio
async def test_film_imdb_sorting(get_request, sorting):
    response = await get_request(f"/film", {"sort": sorting})
    assert response.status == 200


films_pages_params = [(1, 200), (3, 200), (10, 200), (-10, 200), (1000, 404)]


@pytest.mark.parametrize("page_number, expected_response_status", films_pages_params)
@pytest.mark.asyncio
async def test_film_pages(get_request, page_number, expected_response_status):
    response = await get_request(f"/film", {"page[number]": page_number})
    assert response.status == expected_response_status


films_len_pages_params = [(1, 1, 200), (10, 10, 200), (100, 100, 200), (100000, 1, 404)]


@pytest.mark.parametrize("page_number, page_len, expected_response_status", films_len_pages_params)
@pytest.mark.asyncio
async def test_film_len_pages(get_request, page_number, page_len, expected_response_status):
    response = await get_request(f"/film", {"page[size]": page_number})
    assert response.status == expected_response_status
    assert len(response.body) == page_len


film_genres = [
    ("b92ef010-5e4c-4fd0-99d6-41b6456272cd", 200),
    ("120a21cf-9097-479e-904a-13dd7198c1dd", 200),
    ("wrong_uuid", 404),
]


@pytest.mark.parametrize("genre_uuid, expected_response_status", film_genres)
@pytest.mark.asyncio
async def test_film_pages(get_request, genre_uuid, expected_response_status):
    response = await get_request(f"/film", {"filter[genre]": genre_uuid})
    assert response.status == expected_response_status


film_query_params = [
    ("Rebellion", 10, 200),
    ("Foxx", 1, 200),
    ("qwerty", 1, 404),
]


@pytest.mark.parametrize("query, page_len, expected_response_status", film_query_params)
@pytest.mark.asyncio
async def test_film_search(get_request, query, page_len, expected_response_status):
    response = await get_request(f"/film/search", {"query": query})
    assert response.status == expected_response_status
    assert len(response.body) == page_len
