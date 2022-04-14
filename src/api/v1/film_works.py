from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Path, Query
from fastapi.requests import Request
from fastapi.routing import APIRouter
from pydantic import parse_obj_as

from core.config import settings
from decorators import cache_result_of_handler
from models.film_works import FilmWorkResponse, FullFilmWorkResponse
from services.film_works import FilmService, get_film_service

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
        page_size: int = Query(settings.default_page_size, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(settings.default_page_number, alias='page[number]', description='Номер страницы.'),
        filter_genre: str = Query(None, alias='filter[genre]', description='Сортировка по жанрам'),
        sort: str = Query(settings.default_sort_for_filmwork, description='Сортировка по полю фильма.'),
) -> list[Optional[FilmWorkResponse]]:
    """Обработчик запроса всех фильмов - с сортировкой, фильтрацией и тд."""

    film_works = await service.get_film_works_from_storage(
        page_size=page_size,
        page_number=page_number,
        filter_genre=filter_genre,
        sort=sort,
    )
    return parse_obj_as(list[FilmWorkResponse], film_works)


@router.get('/search/', response_model=list[FilmWorkResponse], response_model_by_alias=False)
@cache_result_of_handler(model=FilmWorkResponse, many=True, expire=settings.film_cache_expire_in_seconds)
async def get_searched_film_works(
        request: Request,
        service: FilmService = Depends(get_film_service),
        page_size: int = Query(settings.default_page_size, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(settings.default_page_number, alias='page[number]', description='Номер страницы.'),
        search_query: str = Query(None, alias='query', description='Поиск по кинопроизведениям.'),
) -> list[Optional[FilmWorkResponse]]:
    """Обработчик запроса на поиск по фильмам.
       Настройки по поисковым полям и т.д. можно найти в core/config.py
    """
    film_works = await service.get_film_works_by_searching(
        page_size=page_size,
        page_number=page_number,
        search_query=search_query,
    )
    return parse_obj_as(list[FilmWorkResponse], film_works)
