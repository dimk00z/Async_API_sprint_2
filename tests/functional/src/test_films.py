import pytest
from testdata.films_test_data import (
    films_genres,
    films_id_params,
    films_pages_params,
    films_query_params,
    films_sorting_params,
    films_len_pages_params,
)


@pytest.mark.parametrize("film_uuid, title, imdb_rating, expected_response_status", films_id_params)
@pytest.mark.asyncio
async def test_film_by_id(get_request, film_uuid, title, imdb_rating, expected_response_status):
    response = await get_request(f"/film/{film_uuid}")
    assert response.status == expected_response_status
    assert response.body.get("title", None) == title
    assert response.body.get("imdb_rating", None) == imdb_rating


@pytest.mark.parametrize("sorting", films_sorting_params)
@pytest.mark.asyncio
async def test_film_imdb_sorting(get_request, sorting):
    response = await get_request(f"/film", {"sort": sorting})
    assert response.status == 200


@pytest.mark.parametrize("page_number, expected_response_status", films_pages_params)
@pytest.mark.asyncio
async def test_film_pages(get_request, page_number, expected_response_status):
    response = await get_request(f"/film", {"page[number]": page_number})
    assert response.status == expected_response_status


@pytest.mark.parametrize("page_number, page_len, expected_response_status", films_len_pages_params)
@pytest.mark.asyncio
async def test_film_len_pages(get_request, page_number, page_len, expected_response_status):
    response = await get_request(f"/film", {"page[size]": page_number})
    assert response.status == expected_response_status
    assert len(response.body) == page_len


@pytest.mark.parametrize("genre_uuid, expected_response_status", films_genres)
@pytest.mark.asyncio
async def test_film_pages(get_request, genre_uuid, expected_response_status):
    response = await get_request(f"/film", {"filter[genre]": genre_uuid})
    assert response.status == expected_response_status


@pytest.mark.parametrize("query, page_len, expected_response_status", films_query_params)
@pytest.mark.asyncio
async def test_film_search(get_request, query, page_len, expected_response_status):
    response = await get_request(f"/film/search", {"query": query})
    assert response.status == expected_response_status
    assert len(response.body) == page_len
