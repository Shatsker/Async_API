from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter

from models.genres import GenreResponse
from services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=GenreResponse, response_model_by_alias=False)
async def get_genre_by_id(
        genre_id: UUID,
        service: GenreService = Depends(get_genre_service),
) -> Optional[GenreResponse]:
    """Получение жанра по id, если жанр отсутствует - ошибка 404."""
    genre = await service.get_genre_by_uuid(genre_id)

    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Genre not found',
        )
    return GenreResponse.parse_obj(genre)


@router.get('', response_model=list[GenreResponse], response_model_by_alias=False)
async def get_genres(
        service: GenreService = Depends(get_genre_service),
) -> list[GenreResponse]:
    """Обработчик запроса всех жанров."""
    genres = await service.get_genres()

    return [GenreResponse.parse_obj(g) for g in genres]
