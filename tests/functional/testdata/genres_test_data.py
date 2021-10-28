import json

genres_id_params = [
    ("3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "Action", 200),
    ("120a21cf-9097-479e-904a-13dd7198c1dd", "Adventure", 200),
    ("b92ef010-5e4c-4fd0-99d6-41b6456272cd", "Fantasy", 200),
    ("b92ef010-f6b1-4f3f-8000-13dd7198c1dd", None, 404),
]


def get_genre_from_file(file_path) -> list:
    data = []
    with open(file_path, encoding="utf-8") as file:
        for row in file:
            data.append(json.loads(row.strip())['_source'])
    return data
