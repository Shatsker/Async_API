import datetime
from typing import Optional

import orjson
from pydantic import BaseModel

from core.utils import orjson_dumps

from .genres import Genre
from .persons import Actor, Director, Writer


class FilmWork(BaseModel):
    """Базовая модель кинопроизведений."""
    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    type: Optional[str]
    creation_date: Optional[datetime.date]
    directors: Optional[list[Director]]
    actors: Optional[list[Actor]]
    writers: Optional[list[Writer]]
    genres: Optional[list[Genre]]
    file_path: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
