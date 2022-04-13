import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import test_settings

SERVICE_URL = test_settings.service_api_url


@dataclass
class HttpResponse:
    body: str
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(
        hosts=(f'{test_settings.elastic_host}:{test_settings.elastic_port}',)
    )
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = aioredis.from_url(
        url=f'redis://{test_settings.redis_host}',
        encoding="utf-8",
    )
    yield client
    await client.close()


@pytest.fixture
def make_get_request():
    async def inner(method: str, params: Optional[dict] = None) -> HttpResponse:
        params = params or {}
        url = SERVICE_URL + test_settings.api_v1_prefix + method
        connector = aiohttp.TCPConnector(limit=10)

        async with aiohttp.ClientSession(connector=connector) as session:
            response = await session.get(url=url, params=params)
            return HttpResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
