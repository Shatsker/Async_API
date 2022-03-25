import orjson
import datetime

from typing import Optional

from pydantic import BaseModel

from .persons import Actor, Writer, Director
from .genres import Genre


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


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
