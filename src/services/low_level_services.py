import json
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.base import BaseCacheService, BaseSearchService


class RedisCacheService(BaseCacheService):
    """Сервис для кеширования данных в редис."""

    def __init__(self, redis: Redis = Depends(get_redis)):
        self.redis = redis

    async def get_cache_by_id(
            self,
            cache_id: str,
            model,
            many: bool = False
    ) -> Optional[BaseModel] or Optional[list[BaseModel]]:
        """Получает кэш по id и парсит с помощью модели, затем возвращает объект модели."""
        cache = await self.redis.get(cache_id)

        if not cache:
            return

        if many:
            return [model.parse_raw(ch) for ch in json.loads(cache)]

        return model.parse_raw(cache)

    async def put_to_cache_by_id(
            self,
            cache_id: str,
            cache_models,
            expire: int,
            many: bool = False
    ):
        """Добавляем фильм из elastic'а в кеш по его id."""

        if many:
            data_for_caching = json.dumps([ch.json() for ch in cache_models])
        else:
            data_for_caching = cache_models.json()

        await self.redis.set(
            cache_id,
            data_for_caching,
            ex=expire,
        )


class ElasticSearchService(BaseSearchService):
    """Сервис для получения данных из Elastic'а."""

    def __init__(self, elastic: AsyncElasticsearch = Depends(get_elastic)):
        """Инициализируем объект с клиентом асинхронного elastic'а."""
        self.elastic = elastic

    async def get_full_data_from_storage(
            self,
            model,
            index_of_docs: str,
            page_size: int = None,
            page_number: int = None,
            sort: str = None,
            filter_by_nested: dict[str, str] = None,
    ) -> Optional[list[BaseModel]]:
        """Достает все данные по модели из elastic'а,
           имеется пагинация, сортировка и фильтрация.
        """
        from_ = None

        if page_number is not None and page_size is not None:
            from_ = self._get_page_offset_for_elastic(page_number, page_size)

        if sort is not None:
            sort = self._get_sort_for_elastic(sort)

        documents = await self.elastic.search(
            index=index_of_docs,
            size=page_size,
            from_=from_,
            sort=sort,
            body=filter_by_nested,
        )
        return [model(**doc['_source']) for doc in documents['hits']['hits']]

    async def get_searched_data_from_storage(
            self,
            page_size: int,
            page_number: int,
            index_of_docs: str,
            search_query: str,
            fields_for_searching: list[str],
            model,
    ) -> Optional[list[BaseModel]]:
        """Получаем данные по поисковому запросу из elastic'а."""
        documents = await self.elastic.search(
            index=index_of_docs,
            size=page_size,
            from_=self._get_page_offset_for_elastic(page_number, page_size),
            body=self._get_query_for_searching_data(
                search_query,
                fields_for_searching,
            )
        )
        return [model(**doc['_source']) for doc in documents['hits']['hits']]

    async def get_data_of_one_model_by_id_from_storage(self, index, model_id, model):
        """Возвращает объект переданной модели из elastic'а по id документа."""
        try:
            document = await self.elastic.get(index.value, model_id)
        except NotFoundError:
            return None
        else:
            return model(**document['_source'])

    @staticmethod
    def _get_sort_for_elastic(sort):
        """Из запроса, где указывается -sort_field(как поле для сортировки) - нам нужно получить:
           sort_field:desc, чтобы elastic мог с этим работать.
        """
        return sort + ':asc' if not sort.startswith('-') else sort.removeprefix('-') + ':desc'

    @staticmethod
    def _get_page_offset_for_elastic(page_number, page_size):
        """Из номера страницы и её размера, рассчитываем offset для elastic'а."""
        return (page_number * page_size) - page_size

    @staticmethod
    def _get_query_for_searching_data(
            search_query: str,
            fields_for_searching: list[str],
    ) -> dict:
        """Возвращает запрос на поиск для elastic'а. Передаем ему поля, по которым
           хотим искать в индексе, а так же сам запрос.
        """
        return {
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fuzziness": "auto",
                    "fields": fields_for_searching,
                }
            }
        }


def get_roles_from_jwt(Authorize: AuthJWT = Depends()):
    return Authorize.get_raw_jwt()['roles']
