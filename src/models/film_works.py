import datetime
import orjson

from typing import Optional

from pydantic import BaseModel, Field

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


class FilmWorkResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: Optional[float]

    class Config:
        allow_population_by_field_name = True


class FullFilmWorkResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    directors: Optional[list[Director]]
    actors: Optional[list[Actor]]
    writers: Optional[list[Writer]]
    genres: Optional[list[Genre]]

    class Config:
        allow_population_by_field_name = True
