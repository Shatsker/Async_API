from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi.params import Depends

from core.enums import ElasticIndexes
from models.genres import Genre
from services.base import BaseServicesMixin
from services.low_level_services import ElasticSearchService


class GenreService(BaseServicesMixin):
    """Сервис для работы с жанрами"""

    async def get_genres(self, ) -> list[Genre]:
        """Получение всех жанров"""
        return await self.search_service.get_full_data_from_storage(
            model=Genre,
            index_of_docs=ElasticIndexes.GENRES.value,
            page_size=500,
            sort='id'
        )

    async def get_genre_by_uuid(self, uuid: UUID) -> Optional[Genre]:
        return await self.search_service.get_data_of_one_model_by_id_from_storage(
            index=ElasticIndexes.GENRES,
            model_id=uuid,
            model=Genre
        )


@lru_cache()
def get_genre_service(
        search_service: ElasticSearchService = Depends(ElasticSearchService),
):
    return GenreService(search_service)
