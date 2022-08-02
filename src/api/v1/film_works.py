from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Path, Query
from fastapi.requests import Request
from fastapi.routing import APIRouter
from pydantic import parse_obj_as

from src.core.config import settings
from src.decorators import cache_result_of_handler
from src.models.film_works import FilmWorkResponse, FullFilmWorkResponse
from src.services.film_works import FilmService, get_film_service
from src.services.low_level_services import get_roles_from_jwt

from .params import PaginatedParams

router = APIRouter()


@router.get('/{film_work_id}', response_model=FullFilmWorkResponse, response_model_by_alias=False)
@cache_result_of_handler(model=FullFilmWorkResponse, expire=settings.film_cache_expire_in_seconds)
async def get_film_by_id(
        request: Request,
        film_work_id: UUID = Path(..., description='UUID кинопроизведения.'),
        service: FilmService = Depends(get_film_service),
) -> Optional[FullFilmWorkResponse]:
    """Получение кинопроизведения по id, если фильм отсутствует - ошибка 404."""
    film_work = await service.get_film_work_by_id(film_work_id)

    if not film_work:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Film was not found',
        )

    return FullFilmWorkResponse.parse_obj(film_work)


@router.get('', response_model=list[FilmWorkResponse], response_model_by_alias=False)
@cache_result_of_handler(model=FilmWorkResponse, expire=settings.film_cache_expire_in_seconds, many=True)
async def get_film_works(
        request: Request,
        service: FilmService = Depends(get_film_service),
        pagination: PaginatedParams = Depends(PaginatedParams),
        filter_genre: str = Query(None, alias='filter[genre]', description='Сортировка по жанрам'),
        sort: str = Query(settings.default_sort_for_filmwork, description='Сортировка по полю фильма.'),
        roles: list[str] = Depends(get_roles_from_jwt),
) -> list[Optional[FilmWorkResponse]]:
    """Обработчик запроса всех фильмов - с сортировкой, фильтрацией,
        пагинацией и тд.
    """
    film_works = await service.get_film_works_from_storage(
        page_size=pagination.page_size,
        page_number=pagination.page_number,
        filter_genre=filter_genre,
        sort=sort,
        roles=roles,
    )
    return parse_obj_as(list[FilmWorkResponse], film_works)


@router.get('/search/', response_model=list[FilmWorkResponse], response_model_by_alias=False)
@cache_result_of_handler(model=FilmWorkResponse, many=True, expire=settings.film_cache_expire_in_seconds)
async def get_searched_film_works(
        request: Request,
        service: FilmService = Depends(get_film_service),
        pagination: PaginatedParams = Depends(PaginatedParams),
        search_query: str = Query(None, alias='query', description='Поиск по кинопроизведениям.'),
) -> list[Optional[FilmWorkResponse]]:
    """Обработчик запроса на поиск по фильмам.
       Настройки по поисковым полям и т.д. можно найти в core/config.py
    """
    film_works = await service.get_film_works_by_searching(
        page_size=pagination.page_size,
        page_number=pagination.page_number,
        search_query=search_query,
    )
    return parse_obj_as(list[FilmWorkResponse], film_works)
