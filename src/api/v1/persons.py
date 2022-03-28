from typing import Optional
from uuid import UUID

from fastapi.params import Depends, Path, Query
from fastapi.routing import APIRouter

from core import config
from models.film_works import FilmWorkForResponse
from models.persons import PersonResponse
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[PersonResponse], response_model_by_alias=False)
async def get_searched_persons(
        service: PersonService = Depends(get_person_service),
        page_size: int = Query(config.DEFAULT_PAGE_SIZE, alias='page[size]', description='Размер страницы.'),
        page_number: int = Query(config.DEFAULT_PAGE_NUMBER, alias='page[number]', description='Номер страницы.'),
        search_query: str = Query(None, alias='query', description='Поиск по имени персоны.'),
) -> list[Optional[PersonResponse]]:
    """Обработчик запроса на поиск персон."""
    persons = await service.search_persons(
        page_size=page_size,
        page_number=page_number,
        search_query=search_query,
    )
    return [PersonResponse.parse_obj(p) for p in persons]


@router.get('/{person_id}', response_model=PersonResponse, response_model_by_alias=False)
async def get_persons_by_id(
        person_id: UUID = Path(..., description='UUID персоны'),
        service: PersonService = Depends(get_person_service),
) -> Optional[PersonResponse]:
    """Обработчик запроса на получение персоны по ID"""
    person = await service.get_person_by_uuid(person_id)
    return PersonResponse.parse_obj(person)


@router.get('/{person_id}/film', response_model=list[FilmWorkForResponse], response_model_by_alias=False)
async def get_persons_film_works(
        person_id: UUID = Path(..., description='UUID персоны'),
        service: PersonService = Depends(get_person_service),
) -> list[FilmWorkForResponse]:
    """Обработчик запроса на получение персоны по ID"""
    film_works = await service.get_person_film_works(person_id)
    return film_works
