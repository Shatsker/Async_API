from typing import Optional

from pydantic import BaseModel, Field


class Genre(BaseModel):
    """Модель жанров в кинопроизведениях."""
    id: str
    name: str


class GenreResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    name: str
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
