from uuid import UUID

import pytest

film_id_params = [
    # запрос к существующим id
    (
        "f92c6b11-3f73-4c3f-a9e3-85b1bb91284b",
        "some_data",
        200,
    ),
    # запрос к несуществующему id
    ("c8cb8aa5-926c-4180-81cb-404e2be58a2c", None, 404),
]


@pytest.mark.parametrize("film_id, expected_data, response_status")
@pytest.mark.asyncio
async def test_film_by_id(film_id: UUID, expected_data: str = "", response_status: int = 200):
    pass
