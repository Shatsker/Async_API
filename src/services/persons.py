from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi.params import Depends

from src.core.config import settings
from src.core.enums import ElasticIndexes
from src.models.film_works import FilmWorkResponse
from src.models.persons import Person
from src.services.base import BaseServicesMixin
from src.services.film_works import get_film_service
from src.services.low_level_services import ElasticSearchService


class PersonService(BaseServicesMixin):
    """Сервис для работы с персонами"""

    async def search_persons(
            self,
            page_size: int,
            page_number: int,
            search_query: str,
    ) -> Optional[list[Person]]:
        """Получение персон по поиску из хранилища или кеша."""
        return await self.search_service.get_searched_data_from_storage(
            model=Person,
            page_size=page_size,
            page_number=page_number,
            search_query=search_query,
            index_of_docs=ElasticIndexes.PERSONS.value,
            fields_for_searching=settings.fields_for_searching_persons,
        )

    async def get_person_by_uuid(self, uuid: UUID) -> Optional[Person]:
        return await self.search_service.get_data_of_one_model_by_id_from_storage(
            index=ElasticIndexes.PERSONS,
            model_id=uuid,
            model=Person
        )

    async def get_person_film_works(self, person_uuid: UUID) -> list[FilmWorkResponse]:
        """Возвращает фильмы по персоне (фильмы в которых участвует данная персона)"""

        film_works = []

        person = await self.search_service.get_data_of_one_model_by_id_from_storage(
            index=ElasticIndexes.PERSONS,
            model_id=person_uuid,
            model=Person
        )

        if not person:
            return film_works

        # определено локально в методе чтобы не вызывать рекурсию зависимостей
        film_service = get_film_service(search_service=self.search_service)

        for film_id in person.film_ids:
            film = await film_service.get_film_work_by_id(str(film_id))
            film_works.append(FilmWorkResponse.parse_obj(film))

        return film_works


@lru_cache()
def get_person_service(
        search_service: ElasticSearchService = Depends(ElasticSearchService),
):
    return PersonService(search_service)
