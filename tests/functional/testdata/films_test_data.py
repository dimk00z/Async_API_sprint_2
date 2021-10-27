films_id_params = [
    (
        "2a090dde-f688-46fe-a9f4-b781a985275e",
        "Star Wars: Knights of the Old Republic",
        9.6,
        200,
    ),
    ("fd78a0e5-d4ec-435e-8994-4ccbdfc4e60b", "Lone Star Restoration", 8.7, 200),
    ("3f8873be-f6b1-4f3f-8a01-873924659851", "Justin Bieber: A Star Was Born", 1, 200),
    ("3f8873be-f6b1-4f3f-8000-873924659851", None, None, 404),
]
films_sorting_params = ["imdb_rating", "-imdb_rating", "wrong_sort"]

films_pages_params = [(1, 200), (3, 200), (10, 200), (-10, 200), (1000, 404)]

films_len_pages_params = [(1, 1, 200), (10, 10, 200), (100, 100, 200), (100000, 1, 404)]

films_genres = [
    ("b92ef010-5e4c-4fd0-99d6-41b6456272cd", 200),
    ("120a21cf-9097-479e-904a-13dd7198c1dd", 200),
    ("wrong_uuid", 404),
]

films_query_params = [
    ("Rebellion", 10, 200),
    ("Foxx", 1, 200),
    ("qwerty", 1, 404),
]
