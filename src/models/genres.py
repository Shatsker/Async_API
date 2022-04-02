from pydantic import Field

from .base import BaseModelConfig, MixinAllowPopulation


class Genre(BaseModelConfig):
    """Модель жанров в кинопроизведениях."""
    id: str
    name: str


class GenreResponse(BaseModelConfig, MixinAllowPopulation):
    uuid: str = Field(..., alias='id')
    name: str
