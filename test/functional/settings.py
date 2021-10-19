from pydantic import Field, BaseSettings
from pydantic.error_wrappers import ValidationError


class ElasticSettings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", env="ELASTIC_HOST")


class RedisSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="REDIS_HOST")
    port: str = Field("6379", env="REDIS_PORT")


def load_test_settings() -> tuple[ElasticSettings, RedisSettings]:
    try:
        return (ElasticSettings(), RedisSettings())
    except ValidationError:
        logging.error("Could load settings from enviromentals or .env")
        raise SystemExit
