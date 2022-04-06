from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest
from aioredis import create_redis_pool
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import test_settings

SERVICE_URL = test_settings.service_api_url


@dataclass
class HttpResponse:
    body: str
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(
        hosts=(f'{test_settings.elastic_host}:{test_settings.elastic_port}', )
    )
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = await create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    yield client
    client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HttpResponse:
        params = params or {}
        url = SERVICE_URL + test_settings.api_v1_prefix + method

        async with session.get(url=url, params=params) as response:
            return HttpResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
