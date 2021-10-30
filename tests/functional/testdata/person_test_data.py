from collections import namedtuple

# /person/{person_uuid}
PersonByUUIDCase = namedtuple(
    "PersonByUUIDCase", ("person_uuid", "expected_status", "expected_body")
)
PERSON_BY_UUID_DATA = [
    PersonByUUIDCase(
        person_uuid="96f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.OK,
        expected_body={
            "uuid": "96f18d84-55e0-4718-b87f-4a9e63544d76",
            "full_name": "George Germanetti",
            "films": [
                {
                    "uuid": "b164fef5-0867-46d8-b635-737e1721f6bf",
                    "title": "Tar with a Star",
                    "role": "director",
                }
            ],
        },
    ),
    PersonByUUIDCase(
        person_uuid="16f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.NOT_FOUND,
        expected_body={"detail": "Person not found"},
    ),
    PersonByUUIDCase(  # validation error
        person_uuid="not-uuid",
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["path", "person_uuid"],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid",
                }
            ]
        },
    ),
]

# /person/{person_uuid}/film
PersonFilmsByUUIDCase = namedtuple(
    "PersonFilmsByUUIDCase", ("person_uuid", "expected_status", "expected_body")
)
PERSON_FILMS_BY_UUID_DATA = [
    PersonFilmsByUUIDCase(
        person_uuid="96f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.OK,
        expected_body=[
            {
                "uuid": "b164fef5-0867-46d8-b635-737e1721f6bf",
                "title": "Tar with a Star",
                "role": "director",
            }
        ],
    ),
    PersonFilmsByUUIDCase(
        person_uuid="16f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.NOT_FOUND,
        expected_body={"detail": "Person not found"},
    ),
    PersonFilmsByUUIDCase(  # validation error
        person_uuid="not-uuid",
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["path", "person_uuid"],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid",
                }
            ]
        },
    ),
]

# /person/search
PersonSearchCase = namedtuple("PersonSearchCase", ("params", "expected_status", "expected_body"))
PERSON_SEARCH_DATA = [
    PersonSearchCase(
        params={},
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["query", "query"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        },
    ),
    PersonSearchCase(
        params={"query": "bad_query"},
        expected_status=HTTPStatus.OK,
        expected_body=[],
    ),
    PersonSearchCase(
        params={"query": "george", "page[size]": 2, "page[number]": 5},
        expected_status=HTTPStatus.OK,
        expected_body=[
            {
                "uuid": "c2631edf-33c3-4729-adda-7a25b51f5f20",
                "full_name": "George Geertsen",
                "films": [
                    {
                        "uuid": "a59f548f-e660-4994-ae5e-ed3c911225d3",
                        "title": "George and the Christmas Star",
                        "role": "actor",
                    }
                ],
            },
            {
                "uuid": "89aa1224-d1fd-417c-8561-6993212ecb48",
                "full_name": "George Lazenby",
                "films": [
                    {
                        "uuid": "38f21901-7dcb-467f-b512-550955c072d2",
                        "title": "Star of Jaipur",
                        "role": "actor",
                    }
                ],
            },
        ],
    ),
]
