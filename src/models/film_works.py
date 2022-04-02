import datetime

from typing import Optional

from pydantic import Field

from .base import BaseModelConfig, MixinAllowPopulation
from .genres import Genre
from .persons import Actor, Director, Writer


class FilmWork(BaseModelConfig):
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


class FilmWorkResponse(BaseModelConfig, MixinAllowPopulation):
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: Optional[float]


class FullFilmWorkResponse(BaseModelConfig, MixinAllowPopulation):
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    directors: Optional[list[Director]]
    actors: Optional[list[Actor]]
    writers: Optional[list[Writer]]
    genres: Optional[list[Genre]]
