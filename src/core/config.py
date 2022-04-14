import os
from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """Настройки проекта."""
    project_name: str = 'movies'

    app_host: str = '0.0.0.0'
    app_port: int = 8000

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379

    film_cache_expire_in_seconds: int = 15 * 60
    person_cache_expire_in_seconds: int = 15 * 60
    genre_cache_expire_in_seconds: int = 15 * 60

    elastic_host: str = '127.0.0.1'
    elastic_port: int = 9200

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    default_page_size: int = 10
    default_page_number: int = 1
    default_sort_for_filmwork: str = 'imdb_rating'

    fields_for_searching_filmworks: list[str] = ['title', 'description', 'genre', 'actors_names', 'writers_names']
    fields_for_searching_persons: list[str] = ['full_name', ]


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf8',
)
