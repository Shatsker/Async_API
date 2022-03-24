from http import HTTPStatus

from typing import Optional

from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query

from core import config
from services.films import get_film_services, FilmService
from models.films.response_films import FullFilmWorkForResponse, FilmWorkForResponse

router = APIRouter()


@router.get('/{film_id}', response_model=FullFilmWorkForResponse)
async def get_film_by_id(
        film_id: str,
        film_services: FilmService = Depends(get_film_services),
) -> Optional[FullFilmWorkForResponse]:
    """Получение кинопроизведения по id, если фильм отсутствует - ошибка 404."""
    film = await film_services.get_film_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Film was not found',
        )
    return FullFilmWorkForResponse.parse_obj(film)


@router.get('', response_model=list[FilmWorkForResponse])
async def get_filmworks(
        services: FilmService = Depends(get_film_services),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
        filter_genre: str = Query(None, alias='filter[genre]', description='Сортировка по жанрам'),
        sort: str = Query(config.DEFAULT_SORT_FOR_FILMWORKS, description='Сортировка по полю фильма.'),
) -> list[Optional[FilmWorkForResponse]]:
    """Обработчик запроса всех фильмов - с сортировкой, фильтрацией и тд."""
    film_works = await services.get_film_works_by_filtering_and_sorting(
        page_size=page_size,
        page_number=page_number,
        filter_genre=filter_genre,
        sort=sort,
    )
    return [FilmWorkForResponse.parse_obj(fw) for fw in film_works]


@router.get('/search/', response_model=list[FilmWorkForResponse])
async def get_searched_filmworks(
        services: FilmService = Depends(get_film_services),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
        search_query: str = Query(None, alias='query', description='Поиск по кинопроизведениям.'),
) -> list[Optional[FilmWorkForResponse]]:
    """Обработчик запроса на поиск по фильмам.
       Настройки по поисковым полям и т.д. можно найти в core/config.py
    """
    film_works = await services.get_film_works_by_searching(
        page_size=page_size,
        page_number=page_number,
        search_query=search_query,
    )
    return [FilmWorkForResponse.parse_obj(fw) for fw in film_works]