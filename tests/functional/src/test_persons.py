from unittest import TestCase

import pytest
from testdata.person_test_data import (
    PERSON_SEARCH_DATA,
    PERSON_BY_UUID_DATA,
    PERSON_FILMS_BY_UUID_DATA,
)

# Для использования функций по типу .assertEqual().
# Позволяет "глубоко" сравнить объекты, например, два dict.
test_case_helper = TestCase()


@pytest.mark.parametrize(
    "person_uuid,expected_status,expected_body", PERSON_BY_UUID_DATA
)
@pytest.mark.asyncio
async def test_person_by_uuid(get_request, person_uuid, expected_status, expected_body):
    """Тесты для получения информации по персоне по UUID."""
    response = await get_request(f"/person/{person_uuid}")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize(
    "person_uuid,expected_status,expected_body", PERSON_FILMS_BY_UUID_DATA
)
@pytest.mark.asyncio
async def test_person_films_by_uuid(
    get_request, person_uuid, expected_status, expected_body
):
    """Тесты для получения фильмов по UUID персоны."""
    response = await get_request(f"/person/{person_uuid}/film")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("params,expected_status,expected_body", PERSON_SEARCH_DATA)
@pytest.mark.asyncio
async def test_person_search(get_request, params, expected_status, expected_body):
    """Тесты поиска по персонам."""
    response = await get_request("/person/search", params=params)

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)
