from typing import Optional
from uuid import UUID

from pydantic import Field

from .base import BaseModelConfig, MixinAllowPopulation


class BasePerson(BaseModelConfig):
    """Базовая модель персоны в кинопроизведениях."""
    id: str
    name: Optional[str]


class Person(BaseModelConfig):
    """Модель всех персон, вне зависимости от роли."""
    id: str
    full_name: Optional[str]
    roles: list[str] = []
    film_ids: list[UUID] = []


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


class PersonResponse(BaseModelConfig, MixinAllowPopulation):
    uuid: str = Field(..., alias='id')
    full_name: Optional[str]
    roles: list[str] = []
    film_ids: list[UUID] = []
