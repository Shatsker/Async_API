import orjson
import datetime

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default = default).decode()


class BasePerson(BaseModel):
    """Базовая модель персоны в кинопроизведениях."""
    id: str
    full_name: str


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
    imdb_rating: float
    description: str = None
    type: str
    creation_date: datetime.date
    directors: list[Director]
    actors: list[Actor]
    writers: list[Writer]
    genres: list[Genre]
    file_path: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
