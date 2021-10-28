from pathlib import Path

import pytest

from testdata.genres_test_data import genres_id_params, get_genre_from_file

parent_dir = Path(__file__).parents[1]
filepath = parent_dir.joinpath("testdata", "indexes", "genres.json")


@pytest.mark.parametrize("uuid, name, expected_response_status", genres_id_params)
@pytest.mark.asyncio
async def test_genre_by_id(get_request, uuid, name, expected_response_status):
    """
    Проверка жанра по uuid
    """
    response = await get_request(f"/genre/{uuid}")
    assert response.status == expected_response_status
    assert response.body.get("name", None) == name


@pytest.mark.asyncio
async def test_genre_list(
        get_request,
):
    """
    Проверка списка жанров
    """
    response = await get_request("/genre")
    assert response.status == 200
    assert response.body == get_genre_from_file(filepath)
