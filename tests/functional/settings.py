from pydantic import Field, BaseSettings

CONNECTIONS_MAX_TIME = 60

ES_INDEXES_FILES = (
    ("movies", "testdata/indexes/movies.json"),
    ("genres", "testdata/indexes/genres.json"),
    ("persons", "testdata/indexes/persons.json"),
)


class Settings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", env="ELASTIC_HOST")
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    async_api_host: str = Field("http://127.0.0.1:8000/api/v1", env="ASYNC_API_HOST")
