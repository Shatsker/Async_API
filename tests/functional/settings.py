from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic.fields import Field

load_dotenv()


class TestSettings(BaseSettings):
    """Настройки для тестов."""
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    app_host: str = Field('0.0.0.0', env='APP_HOST')
    app_port: int = Field(8000, env='APP_PORT')

    elastic_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    elastic_port: int = Field(9200, env='ELASTIC_PORT')

    service_api_url: str = 'http://0.0.0.0:8000'
    api_v1_prefix: str = '/api/v1'


test_settings = TestSettings()
