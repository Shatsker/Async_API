from pydantic import BaseModel


class Genre(BaseModel):
    """Модель жанров в кинопроизведениях."""
    id: str
    name: str
