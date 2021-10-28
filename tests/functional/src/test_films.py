import pytest
from testdata.films_test_data import (
    FILMS_GENRES,
    FILM_SEARCH_DATA,
    FILM_BY_UUID_DATA,
    FILMS_PAGES_PARAMS,
    FILMS_SORTING_PARAMS,
    FILMS_LEN_PAGES_PARAMS,
)


@pytest.mark.parametrize("film_uuid,expected_status,expected_body", FILM_BY_UUID_DATA)
@pytest.mark.asyncio
async def test_film_by_uuid(
    get_request, test_case_helper, film_uuid, expected_status, expected_body
):
    response = await get_request(f"/film/{film_uuid}")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("params,expected_status,expected_body", FILM_SEARCH_DATA)
@pytest.mark.asyncio
async def test_film_search(
    get_request, test_case_helper, params, expected_status, expected_body
):
    response = await get_request("/film/search", params=params)

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("sorting", FILMS_SORTING_PARAMS)
@pytest.mark.asyncio
async def test_film_imdb_sorting(get_request, sorting):
    response = await get_request(f"/film", {"sort": sorting})
    assert response.status == 200


@pytest.mark.parametrize("page_number, expected_response_status", FILMS_PAGES_PARAMS)
@pytest.mark.asyncio
async def test_film_pages(get_request, page_number, expected_response_status):
    response = await get_request(f"/film", {"page[number]": page_number})
    assert response.status == expected_response_status


@pytest.mark.parametrize(
    "page_number, page_len, expected_response_status", FILMS_LEN_PAGES_PARAMS
)
@pytest.mark.asyncio
async def test_film_len_pages(
    get_request, page_number, page_len, expected_response_status
):
    response = await get_request(f"/film", {"page[size]": page_number})
    assert response.status == expected_response_status
    assert len(response.body) == page_len


@pytest.mark.parametrize("genre_uuid, expected_response_status", FILMS_GENRES)
@pytest.mark.asyncio
async def test_film_genre_sort(get_request, genre_uuid, expected_response_status):
    response = await get_request(f"/film", {"filter[genre]": genre_uuid})
    assert response.status == expected_response_status
