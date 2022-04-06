import asyncio

from aioredis import create_redis_pool
from settings import test_settings


async def wait_for_redis():
    """Функция ожидания подъёма redis'а перед тестами."""
    redis = await create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20,
    )

    while True:
        if await redis.ping() == b'PONG':
            redis.close()
            break

        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_redis())
