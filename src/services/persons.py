from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi.params import Depends

from core import config
from core.enums import ElasticIndexes
from models.persons import Person
from services.base import BaseServicesMixin
from services.low_level_services import ElasticSearchService, RedisCacheService


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
            fields_for_searching=config.FIELDS_FOR_SEARCHING_PERSONS,
        )

    async def get_person_by_uuid(self, uuid: UUID) -> Optional[Person]:
        return await self.search_service.get_data_of_one_model_by_id_from_storage(
            index=ElasticIndexes.PERSONS,
            model_id=uuid,
            model=Person
        )


@lru_cache()
def get_person_service(
        redis: RedisCacheService = Depends(RedisCacheService),
        elastic: ElasticSearchService = Depends(ElasticSearchService),
):
    return PersonService(redis, elastic)
