from functools import wraps

from fastapi.requests import Request

from src.db.redis import get_redis
from src.services.low_level_services import RedisCacheService


def cache_result_of_handler(model, expire: int, many=False):
    """Декоратор для кеширования результата обработчика.
    Arguments:
        model: Pydantic-модель которую возвращает обработчик
        many: Передаётся список моделей, или одиночная модель
        expire: Время жизни кеша
    Returns:
        Результат работы обработчика, или кеш этого же результата.
    """
    def handler_decorator(handler):
        @wraps(handler)
        async def wrapper(request: Request, *args, **kwargs):
            key_for_cache = str(request.url)
            cache_service = RedisCacheService(await get_redis())
            cache_of_handler = await cache_service.get_cache_by_id(
                cache_id=key_for_cache,
                model=model,
                many=many,
            )

            if cache_of_handler:
                return cache_of_handler

            if not cache_of_handler:
                data_from_handler = await handler(request, *args, **kwargs)
                await cache_service.put_to_cache_by_id(
                    cache_id=key_for_cache,
                    cache_models=data_from_handler,
                    expire=expire,
                    many=many,
                )
                return data_from_handler

        return wrapper
    return handler_decorator
