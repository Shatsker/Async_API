from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi import Depends

from src.core.config import settings
from src.core.enums import ElasticIndexes
from src.models.film_works import FilmWork
from src.queries.es.film_work.nested_search import get_nested_search_query_by_genre
from src.services.base import BaseServicesMixin
from src.services.low_level_services import ElasticSearchService


class FilmService(BaseServicesMixin):
    """Класс, для бизнес-логики к фильмам."""

    async def get_film_works_from_storage(
            self,
            page_size: Optional[int],
            page_number: Optional[int],
            filter_genre: Optional[str],
            sort: Optional[str],
            roles: Optional[list[str]],
    ) -> Optional[list[FilmWork]]:
        """Возвращает фильмы, есть пагинация, сортировка & фильтрация.
           Достаёт из кеша или elastic'а, если кеш пуст.
        """
        return await self.search_service.get_full_data_from_storage(
            sort=sort,
            model=FilmWork,
            page_size=page_size,
            page_number=page_number,
            index_of_docs=ElasticIndexes.MOVIES.value,
            filter_by_nested=get_nested_search_query_by_genre(filter_genre),
        )

    async def get_film_works_by_searching(
            self,
            page_size: int,
            page_number: int,
            search_query: str,
    ) -> Optional[list[FilmWork]]:
        """Получение фильмов по поиску из хранилища или кеша."""
        return await self.search_service.get_searched_data_from_storage(
            model=FilmWork,
            page_size=page_size,
            page_number=page_number,
            search_query=search_query,
            index_of_docs=ElasticIndexes.MOVIES.value,
            fields_for_searching=settings.fields_for_searching_filmworks,
        )

    async def get_film_work_by_id(self, film_work_id: UUID) -> Optional[FilmWork]:
        """Возвращает фильм по id из кеша, или из хранилища.
           Если фильма нет - возвращает None.
        """
        return await self.search_service.get_data_of_one_model_by_id_from_storage(
            index=ElasticIndexes.MOVIES,
            model_id=film_work_id,
            model=FilmWork,
        )


@lru_cache()
def get_film_service(
        search_service: ElasticSearchService = Depends(ElasticSearchService),
):
    return FilmService(search_service)
