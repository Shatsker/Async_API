from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel
from pydantic.fields import Field

from core.utils import orjson_dumps


class BasePerson(BaseModel):
    """Базовая модель персоны в кинопроизведениях."""
    id: str
    name: Optional[str]


class Person(BaseModel):
    """Модель всех персон, вне зависимости от роли."""
    uuid: str = Field(..., alias='id')
    full_name: Optional[str]
    roles: list[str] = []
    film_ids: list[UUID] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


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
