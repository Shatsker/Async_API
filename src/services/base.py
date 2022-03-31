from abc import ABC, abstractmethod
from typing import Union
from uuid import UUID

from core.enums import ElasticIndexes


class BaseCacheService(ABC):
    """Абстрактный класс для сервиса кеширования."""

    @abstractmethod
    def get_cache_by_id(self, *args, **kwargs):
        """Метод для получения кеша по id сущности."""
        pass

    @abstractmethod
    def put_to_cache_by_id(self, *args, **kwargs):
        """Метод для вставки кеша по id сущности."""
        pass


class BaseSearchService(ABC):
    """Абстрактный класс для сервиса поиска."""

    @abstractmethod
    def get_full_data_from_storage(self, *args, **kwargs):
        """Метод для получения данных из хранилища."""
        pass

    @abstractmethod
    def get_data_of_one_model_by_id_from_storage(
            self,
            index: ElasticIndexes,
            model_id: Union[str, UUID],
            model
    ):
        pass

    @abstractmethod
    def get_searched_data_from_storage(self, *args, **kwargs):
        """Метод для получения данных по поиску из хранилища."""
        pass


class BaseServicesMixin:
    """Миксин с поиском."""

    def __init__(self, search_service: BaseSearchService):
        self.search_service = search_service
