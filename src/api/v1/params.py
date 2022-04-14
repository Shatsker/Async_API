from fastapi import Query

from src.core.config import settings


class PaginatedParams:
    """Параметры для пагинации во вьюхах."""
    def __init__(
            self,
            page_size: int = Query(
                settings.default_page_size,
                alias='page[size]',
                description='Размер страницы.',
            ),
            page_number: int = Query(
                settings.default_page_number,
                alias='page[number]',
                description='Номер страницы.',
            )
    ):
        self.page_size = page_size
        self.page_number = page_number
