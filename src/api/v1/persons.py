from typing import Optional
from uuid import UUID
from http import HTTPStatus

from fastapi.params import Depends, Path, Query
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.exceptions import HTTPException

from pydantic import parse_obj_as

from core.config import settings
from decorators import cache_result_of_handler
from models.film_works import FilmWorkResponse
from models.persons import PersonResponse
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[PersonResponse], response_model_by_alias=False)
@cache_result_of_handler(model=PersonResponse, expire=settings.person_cache_expire_in_seconds, many=True)
async def get_searched_persons(
        request: Request,
        service: PersonService = Depends(get_person_service),
        page_size: int = Query(settings.default_page_size, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(settings.default_page_number, alias='page[number]', description='Номер страницы.'),
        search_query: str = Query(None, alias='query', description='Поиск по имени персоны.'),
) -> list[Optional[PersonResponse]]:
    """Обработчик запроса на поиск персон."""
    persons = await service.search_persons(
        page_size=page_size,
        page_number=page_number,
        search_query=search_query,
    )
    return parse_obj_as(list[PersonResponse], persons)


@router.get('/{person_id}', response_model=PersonResponse, response_model_by_alias=False)
@cache_result_of_handler(model=PersonResponse, expire=settings.person_cache_expire_in_seconds)
async def get_persons_by_id(
        request: Request,
        person_id: UUID = Path(..., description='UUID персоны'),
        service: PersonService = Depends(get_person_service),
) -> Optional[PersonResponse]:
    """Обработчик запроса на получение персоны по ID"""
    person = await service.get_person_by_uuid(person_id)

    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Person was not found',
        )

    return PersonResponse.parse_obj(person)


@router.get('/{person_id}/film', response_model=list[FilmWorkResponse], response_model_by_alias=False)
@cache_result_of_handler(model=FilmWorkResponse, expire=settings.person_cache_expire_in_seconds, many=True)
async def get_persons_film_works(
        request: Request,
        person_id: UUID = Path(..., description='UUID персоны'),
        service: PersonService = Depends(get_person_service),
) -> list[FilmWorkResponse]:
    """Обработчик запроса на получение фильмов по ID персоны"""
    film_works = await service.get_person_film_works(person_id)
    return film_works
