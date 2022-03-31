from http import HTTPStatus
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from fastapi.routing import APIRouter
from fastapi.requests import Request

from core import config
from decorators import cache_result_of_handler
from models.film_works import FilmWorkResponse, FullFilmWorkResponse
from services.film_works import FilmService, get_film_service

router = APIRouter()


@router.get('/{film_id}', response_model=FullFilmWorkResponse, response_model_by_alias=False)
@cache_result_of_handler(model=FullFilmWorkResponse)
async def get_film_by_id(
        request: Request,
        film_id: str,
        service: FilmService = Depends(get_film_service),
) -> Optional[FullFilmWorkResponse]:
    """Получение кинопроизведения по id, если фильм отсутствует - ошибка 404."""
    film = await service.get_film_work_by_id(film_id)

    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Film was not found',
        )

    return FullFilmWorkResponse.parse_obj(film)


@router.get('', response_model=list[FilmWorkResponse], response_model_by_alias=False)
@cache_result_of_handler(model=FilmWorkResponse, many=True)
async def get_film_works(
        request: Request,
        service: FilmService = Depends(get_film_service),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
        filter_genre: str = Query(None, alias='filter[genre]', description='Сортировка по жанрам'),
        sort: str = Query(config.DEFAULT_SORT_FOR_FILMWORKS, description='Сортировка по полю фильма.'),
) -> list[Optional[FilmWorkResponse]]:
    """Обработчик запроса всех фильмов - с сортировкой, фильтрацией и тд."""
    film_works = await service.get_film_works_from_storage_or_cache(
        page_size=page_size,
        page_number=page_number,
        filter_genre=filter_genre,
        sort=sort,
    )
    return [FilmWorkResponse.parse_obj(fw) for fw in film_works]


@router.get('/search/', response_model=list[FilmWorkResponse], response_model_by_alias=False)
@cache_result_of_handler(model=FilmWorkResponse, many=True)
async def get_searched_film_works(
        request: Request,
        service: FilmService = Depends(get_film_service),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
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
    return [FilmWorkResponse.parse_obj(fw) for fw in film_works]
