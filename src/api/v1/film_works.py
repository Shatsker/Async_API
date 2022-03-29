from http import HTTPStatus

from typing import Optional

from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from fastapi.requests import Request

from core import config
from decorators import cache_result_of_handler
from services.film_works import get_film_services, FilmService
from models.response_models import FullFilmWorkForResponse, FilmWorkForResponse

router = APIRouter()


@router.get('/{film_work_id}', response_model=FullFilmWorkForResponse)
@cache_result_of_handler(model=FullFilmWorkForResponse)
async def get_film_by_id(
        request: Request,
        film_work_id: str,
        service: FilmService = Depends(get_film_services),
) -> Optional[FullFilmWorkForResponse]:
    """Получение кинопроизведения по id, если фильм отсутствует - ошибка 404."""
    film_work = await service.get_film_work_by_id(film_work_id=film_work_id)
    if not film_work:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Film was not found',
        )
    return FullFilmWorkForResponse.parse_obj(film_work)


@router.get('', response_model=list[FilmWorkForResponse])
@cache_result_of_handler(model=FilmWorkForResponse, many=True)
async def get_film_works(
        request: Request,
        service: FilmService = Depends(get_film_services),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
        filter_genre: str = Query(None, alias='filter[genre]', description='Сортировка по жанрам'),
        sort: str = Query(config.DEFAULT_SORT_FOR_FILMWORKS, description='Сортировка по полю фильма.'),
) -> list[Optional[FilmWorkForResponse]]:
    """Обработчик запроса всех фильмов - с сортировкой, фильтрацией и тд."""
    film_works = await service.get_film_works_from_storage_or_cache(
        page_size=page_size,
        page_number=page_number,
        filter_genre=filter_genre,
        sort=sort,
    )
    return [FilmWorkForResponse.parse_obj(fw) for fw in film_works]


@router.get('/search/', response_model=list[FilmWorkForResponse])
@cache_result_of_handler(model=FilmWorkForResponse, many=True)
async def get_searched_film_works(
        request: Request,
        service: FilmService = Depends(get_film_services),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
        search_query: str = Query(None, alias='query', description='Поиск по кинопроизведениям.'),
) -> list[Optional[FilmWorkForResponse]]:
    """Обработчик запроса на поиск по фильмам.
       Настройки по поисковым полям и т.д. можно найти в core/config.py
    """
    film_works = await service.get_film_works_by_searching(
        page_size=page_size,
        page_number=page_number,
        search_query=search_query,
    )
    return [FilmWorkForResponse.parse_obj(fw) for fw in film_works]
