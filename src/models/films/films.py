import orjson
import datetime

from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BasePerson(BaseModel):
    """Базовая модель персоны в кинопроизведениях."""
    id: str
    name: Optional[str]


class Person(BasePerson):
    """Модель всех персон, вне зависимости от роли."""
    role: str
    film_ids: list[str] = None


class Actor(BasePerson):
    """Модель актеров в кинопроизведениях.
       Сюда можно заносить какие-то специфичные для актеров поля.
    """
    pass


class Director(BasePerson):
    """Модель режиссёров в кинопроизведениях.
       Сюда можно заносить какие-то специфичные для режиссеров поля.
    """
    pass


class Writer(BasePerson):
    """Модель сценаристов в кинопроизведениях.
       Сюда можно заносить какие-то специфичные для сценаристов поля.
    """
    pass


class Genre(BaseModel):
    """Модель жанров в кинопроизведениях."""
    id: str
    name: str


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
