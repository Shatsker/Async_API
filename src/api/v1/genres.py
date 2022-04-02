from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request

from pydantic import parse_obj_as

from core.config import settings
from decorators import cache_result_of_handler
from models.genres import GenreResponse
from services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=GenreResponse, response_model_by_alias=False)
@cache_result_of_handler(model=GenreResponse, expire=settings.genre_cache_expire_in_seconds)
async def get_genre_by_id(
        request: Request,
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
@cache_result_of_handler(model=GenreResponse, expire=settings.genre_cache_expire_in_seconds, many=True)
async def get_genres(
        request: Request,
        service: GenreService = Depends(get_genre_service),
) -> list[GenreResponse]:
    """Обработчик запроса всех жанров."""
    genres = await service.get_genres()

    return parse_obj_as(list[GenreResponse], genres)
