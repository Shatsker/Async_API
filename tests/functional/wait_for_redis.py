import asyncio

import aioredis
from settings import test_settings


async def wait_for_redis():
    """Функция ожидания подъёма redis'а перед тестами."""
    print(1)
    redis = await aioredis.from_url(
        f'redis://{test_settings.redis_host}',
        encoding="utf-8",
        decode_responses=True,
    )
    print(2)

    while True:
        if await redis.ping() == b'PONG':
            redis.close()
            break

        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_redis())
