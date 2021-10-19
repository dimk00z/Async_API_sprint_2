from pydantic import Field, BaseSettings
from pydantic.error_wrappers import ValidationError


class TestSettings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", env="ELASTIC_HOST")
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")
    async_api_host: str = Field("http://127.0.0.1:8000/api/v1", env="ASYNC_API_HOST")
