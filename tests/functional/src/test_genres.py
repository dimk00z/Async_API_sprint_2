from unittest import TestCase

import pytest
from testdata.genre_test_data import (
    GENRE_BY_UUID_DATA, GENRE_DATA)

# Для использования функций по типу .assertEqual().
# Позволяет "глубоко" сравнить объекты, например, два dict.
test_case_helper = TestCase()


@pytest.mark.parametrize(
    "genre_uuid,expected_status,expected_body", GENRE_BY_UUID_DATA
)
@pytest.mark.asyncio
async def test_genre_by_uuid(get_request, genre_uuid, expected_status, expected_body):
    """Тесты для получения информации по жанру по UUID."""
    response = await get_request(f"/genre/{genre_uuid}")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("expected_status,expected_body", GENRE_DATA)
@pytest.mark.asyncio
async def test_genre_list(get_request, expected_status, expected_body):
    """Тесты получения жанров."""
    response = await get_request("/genre")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)
