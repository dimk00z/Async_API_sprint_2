from collections import namedtuple

FilmByUUIDCase = namedtuple("FilmByUUIDCase", ("film_uuid", "expected_status", "expected_body"))

FILM_BY_UUID_DATA = [
    FilmByUUIDCase(
        film_uuid="2a090dde-f688-46fe-a9f4-b781a985275e",
        expected_status=200,
        expected_body={
            "uuid": "2a090dde-f688-46fe-a9f4-b781a985275e",
            "title": "Star Wars: Knights of the Old Republic",
            "description": "Four thousand years before the fall of the Republic, before the fall of the Jedi, a great war was fought, between the armies of the Sith and the forces of the Republic. A warrior is chosen to rescue a Jedi with a power important to the cause of the Republic, but in the end, will the warrior fight for the Light Side of the Force, or succumb to the Darkness?",
            "imdb_rating": 9.6,
            "genres": [
                {"uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"},
                {"uuid": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"},
                {"uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
            ],
            "writers": [
                {"uuid": "b29e255d-644d-4e16-9018-c1bcb49934e5", "full_name": "Lynn Taylor"},
                {"uuid": "63a787ba-dd3f-4176-a894-9970b5c43a12", "full_name": "Drew Karpyshyn"},
                {"uuid": "f7337af0-21aa-445f-aecf-4794c0faa811", "full_name": "Brett Rector"},
                {"uuid": "1bc82e3e-d9ea-4da0-a5ea-69ba20b94373", "full_name": "Lukas Kristjanson"},
                {"uuid": "61bffbdc-910e-47b9-8b04-43b5f27807b4", "full_name": "James Ohlen"},
                {"uuid": "8778550c-90c6-4180-a6ac-eba956f0ce59", "full_name": "David Gaider"},
                {"uuid": "91c4ca66-e3e1-4932-8447-aadd67fd67b1", "full_name": "Peter Thomas"},
                {"uuid": "1e8d746d-72d2-4da2-ad20-651154cfb158", "full_name": "Michael Gallo"},
            ],
            "actors": [
                {"uuid": "00395304-dd52-4c7b-be0d-c2cd7a495684", "full_name": "Jennifer Hale"},
                {"uuid": "578593ee-3268-4cd4-b910-8a44cfd05b73", "full_name": "Rafael Ferrer"},
                {"uuid": "bccbbbb6-be40-44f5-a025-204bcfcf2667", "full_name": "Raphael Sbarge"},
                {"uuid": "2802ff93-f147-49cc-a38b-2f787bd2b875", "full_name": "John Cygan"},
            ],
            "directors": [
                {"uuid": "1a9e7e1f-393b-455d-a76f-d3ad2b33673e", "full_name": "Casey Hudson"}
            ],
        },
    ),
    FilmByUUIDCase(
        film_uuid="3f8873be-f6b1-4f3f-8a01-873924659851",
        expected_status=200,
        expected_body={
            "uuid": "3f8873be-f6b1-4f3f-8a01-873924659851",
            "title": "Justin Bieber: A Star Was Born",
            "description": None,
            "imdb_rating": 1,
            "genres": [
                {"uuid": "56b541ab-4d66-4021-8708-397762bff2d4", "name": "Music"},
                {"uuid": "6d141ad2-d407-4252-bda4-95590aaf062a", "name": "Documentary"},
            ],
            "writers": None,
            "actors": [
                {"uuid": "a967bacf-35ca-42ef-9bfd-3d003a957125", "full_name": "Justin Bieber"}
            ],
            "directors": None,
        },
    ),
    FilmByUUIDCase(
        film_uuid="3f8873be-f6b1-4f3f-8000-873924659851",
        expected_status=404,
        expected_body={"detail": "film not found"},
    ),
    FilmByUUIDCase(
        film_uuid="wrong-uuid",
        expected_status=422,
        expected_body={
            "detail": [
                {
                    "loc": ["path", "film_uuid"],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid",
                }
            ]
        },
    ),
]

FilmSearchCase = namedtuple("FilmSearchCase", ("params", "expected_status", "expected_body"))

FILM_SEARCH_DATA = [
    FilmSearchCase(
        params={"query": "bad_query"},
        expected_status=404,
        expected_body={"detail": "not one film found"},
    ),
    FilmSearchCase(
        params={"query": "Bieber"},
        expected_status=200,
        expected_body=[
            {
                "uuid": "3f8873be-f6b1-4f3f-8a01-873924659851",
                "title": "Justin Bieber: A Star Was Born",
                "imdb_rating": 1,
            }
        ],
    ),
    FilmSearchCase(
        params={"query": "Birth"},
        expected_status=200,
        expected_body=[
            {
                "uuid": "26d9ff12-5110-4ab4-bb04-a4ca55729503",
                "title": "Star Trek: Birth of the Federation",
                "imdb_rating": 8.4,
            },
            {
                "uuid": "4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f",
                "title": "Star Trek",
                "imdb_rating": 7.9,
            },
            {
                "uuid": "7a25c172-c846-48b6-8cb4-e9003b786937",
                "title": "Prelude: Dog Star Man",
                "imdb_rating": 6.9,
            },
            {
                "uuid": "231583e8-50bd-4e4d-8514-325b4bb8a61e",
                "title": "Prelude: Dog Star Man",
                "imdb_rating": 6.7,
            },
            {
                "uuid": "a6187fa4-56e9-4fb4-8fba-ca9b27ace656",
                "title": "Star Trek Secret Voyage: Whose Birth These Triumphs Are",
                "imdb_rating": 5.9,
            },
            {
                "uuid": "9a233936-915e-4e8a-99bb-5d94a1d9eeca",
                "title": "Shuten Doji: The Star Hand Kid 2 - Demon Battle in the Firefly Field",
                "imdb_rating": 5.5,
            },
        ],
    ),
]

FilmRatingSortCase = namedtuple("FilmRatingSortCase", ("sorting",))

FILMS_SORTING_PARAMS = (
    FilmRatingSortCase(sorting="imdb_rating"),
    FilmRatingSortCase(sorting="-imdb_rating"),
    FilmRatingSortCase(sorting="wrong_sort"),
)

FilmPageCase = namedtuple("FilmPageCase", ("page_number", "expected_status"))

FILMS_PAGES_PARAMS = (
    FilmPageCase(page_number=1, expected_status=200),
    FilmPageCase(page_number=2, expected_status=200),
    FilmPageCase(page_number=10, expected_status=200),
    FilmPageCase(page_number=-10, expected_status=200),
    FilmPageCase(page_number=1000, expected_status=404),
)
FilmLenPagesCase = namedtuple("FilmLenPagesCase", ("page_number", "page_len", "expected_status"))

FILMS_LEN_PAGES_PARAMS = [
    FilmLenPagesCase(page_number=1, page_len=1, expected_status=200),
    FilmLenPagesCase(page_number=10, page_len=10, expected_status=200),
    FilmLenPagesCase(page_number=100, page_len=100, expected_status=200),
    FilmLenPagesCase(page_number=100000, page_len=1, expected_status=404),
]
FilmGenresCase = namedtuple("FilmGenresCase", ("genre_uuid", "expected_response_status"))

FILMS_GENRES = [
    FilmGenresCase(genre_uuid="b92ef010-5e4c-4fd0-99d6-41b6456272cd", expected_response_status=200),
    FilmGenresCase(genre_uuid="120a21cf-9097-479e-904a-13dd7198c1dd", expected_response_status=200),
    FilmGenresCase(genre_uuid="wrong_uuid", expected_response_status=404),
]
