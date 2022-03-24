from pydantic import BaseModel

from typing import Optional

from .films import Actor, Writer, Genre, Director


class FilmWorkForResponse(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class FullFilmWorkForResponse(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    directors: Optional[list[Director]]
    actors: Optional[list[Actor]]
    writers: Optional[list[Writer]]
    genres: Optional[list[Genre]]
