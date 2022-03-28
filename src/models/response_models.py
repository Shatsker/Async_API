from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from models.film_works import Actor, Director, Genre, Writer


class FilmWorkForResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: Optional[float]


class FullFilmWorkForResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    directors: Optional[list[Director]]
    actors: Optional[list[Actor]]
    writers: Optional[list[Writer]]
    genres: Optional[list[Genre]]


class PersonResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    full_name: Optional[str]
    roles: list[str] = []
    film_ids: list[UUID] = []


class GenreResponse(BaseModel):
    uuid: str = Field(..., alias='id')
    name: str
    description: Optional[str]
