from pydantic import BaseModel

from typing import Optional


class BasePerson(BaseModel):
    """Базовая модель персоны в кинопроизведениях."""
    id: str
    name: Optional[str]


class Person(BasePerson):
    """Модель всех персон, вне зависимости от роли."""
    role: list[str] = None
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
