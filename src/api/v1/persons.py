from typing import Optional

from fastapi.params import Depends, Query
from fastapi.routing import APIRouter

from core import config
from models.response_models import PersonResponse
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get('/search/', response_model=list[PersonResponse])
async def get_searched_film_works(
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
