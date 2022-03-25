import os
from logging import config as logging_config

from dotenv import load_dotenv

from core.logger import LOGGING

load_dotenv()
logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'shatsker_movies')

APP_HOST = os.getenv('APP_HOST', '0.0.0.0')

APP_PORT = int(os.getenv('APP_PORT', 8000))

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1
DEFAULT_SORT_FOR_FILMWORKS = 'imdb_rating'

FIELDS_FOR_SEARCHING_FILMWORK = ['title', 'description', 'genre', 'actors_names', 'writers_names']
