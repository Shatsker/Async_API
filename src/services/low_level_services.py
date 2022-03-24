from typing import Optional
from abc import ABC

from aioredis import Redis

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from fastapi.params import Depends
from pydantic import BaseModel

from db.redis import get_redis
from db.elastic import get_elastic
from core import config

from .base import BaseCacheService, BaseSearchService


class RedisCacheService(BaseCacheService, ABC):
    """Сервис для кеширования данных в редис."""

    def __init__(self, redis: Redis = Depends(get_redis)):
        self.redis = redis

    async def get_cache_by_id(self, cache_id: str, model) -> Optional[BaseModel]:
        """Получает кэш по id и парсит с помощью модели, затем возвращает объект модели."""
        cache = await self.redis.get(cache_id)
        if cache:
            return model.parse_raw(cache)

    async def put_to_cache_by_id(self, model_for_caching: BaseModel):
        """Добавляем фильм из elastic'а в кеш по его id."""
        await self.redis.set(
            model_for_caching.id,
            model_for_caching.json(),
            expire=config.FILM_CACHE_EXPIRE_IN_SECONDS,
        )


class ElasticSearchService(BaseSearchService, ABC):
    """Сервис для получения данных из Elastic'а."""

    def __init__(self, elastic: AsyncElasticsearch = Depends(get_elastic)):
        """Инициализируем объект с клиентом асинхронного elastic'а."""
        self.elastic = elastic

    async def get_full_data_from_storage(
            self,
            page_size: int,
            page_number: int,
            filter_by_nested: Optional[dict[str, str]],
            index_of_docs: str,
            sort: str,
            model,
    ) -> Optional[list[BaseModel]]:
        """Достает все данные по модели из elastic'а,
           имеется пагинация, сортировка и фильтрация.
        """
        documents = await self.elastic.search(
            index=index_of_docs,
            size=page_size,
            from_=self._get_page_offset_for_elastic(page_number, page_size),
            sort=self._get_sort_for_elastic(sort),
            body=self._get_query_for_getting_fw_by_id_of_nested_object_in_elastic(
                filter_by_nested
            ) if filter_by_nested else None,
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

    async def get_data_of_one_model_by_id_from_storage(self, model_id, model):
        """Возвращает объект переданной модели из elastic'а по id документа."""
        try:
            document = await self.elastic.get('movies', model_id)
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

    @staticmethod
    def _get_query_for_getting_fw_by_id_of_nested_object_in_elastic(
            filter_info: dict[str, str],
    ) -> Optional[dict]:
        """Получаем фильмы с переданным названием nested_object'а в elastic'е
           и значением его id.
        """
        nested_obj_name = filter_info.get('name', None)
        nested_obj_value = filter_info.get('value', None)
        if nested_obj_name and nested_obj_value:
            return {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "nested": {
                                    "path": nested_obj_name,
                                    "query": {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match": {
                                                        f"{nested_obj_name}.id": nested_obj_value
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
