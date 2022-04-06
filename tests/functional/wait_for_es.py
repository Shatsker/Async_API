import asyncio

from elasticsearch import AsyncElasticsearch
from settings import test_settings


async def wait_for_elastic():
    """Функция ожидания подъёма elasctic'а перед тестами."""
    es_client = AsyncElasticsearch(
        hosts=f'{test_settings.elastic_host}:{test_settings.elastic_port}'
    )

    while True:
        if await es_client.ping():
            await es_client.close()
            break

        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_elastic())
