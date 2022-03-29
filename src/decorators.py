from functools import wraps

from fastapi.requests import Request

from services.low_level_services import RedisCacheService
from db.redis import get_redis


def cache_result_of_handler(model, many=False):
    """Декоратор для кеширования результата обработчика.
    Arguments:
        model: Pydantic-модель которую возвращает обработчик
        many: Передаётся список моделей, или одиночная модель
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
            if not cache_of_handler:
                data_from_handler = await handler(request, *args, **kwargs)
                await cache_service.put_to_cache_by_id(
                    cache_id=key_for_cache,
                    cache=data_from_handler,
                    many=many,
                )
                return data_from_handler
            else:
                return cache_of_handler

        return wrapper
    return handler_decorator
