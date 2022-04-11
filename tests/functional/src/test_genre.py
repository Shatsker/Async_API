import json

import pytest

from models.genres import GenreResponse
from tests.functional.conftest import SERVICE_URL
from tests.functional.settings import test_settings
from tests.functional.testdata.genre import ALL_GENRES

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает из ES жанр по uuid""",
            {
                'method': '/genres/120a21cf-9097-479e-904a-13dd7198c1dd',
            },
            {
                "uuid": "120a21cf-9097-479e-904a-13dd7198c1dd",
                "name": "Adventure"
            },
        ],
        [
            """Получает из ES жанр по uuid, но такого uuid у нас нет - валимся в 404""",
            {
                'method': '/genres/120a21cf-9027-479e-904a-13dd7198c1dd',
            },
            {'detail': 'Genre not found'},
        ],
    ]

)
async def test_get_genre_by_id_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_request
):
    response = await make_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_get_genre_by_id_with_redis_handler(
        es_client, redis_client, make_request
):
    should_be = {"uuid": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"}

    # кидаем запрос и ждем что ответ окажется в redis
    await make_request(method='/genres/120a21cf-9097-479e-904a-13dd7198c1dd')
    redis_data = await redis_client.get(
        key=f'{SERVICE_URL}{test_settings.api_v1_prefix}/genres/120a21cf-9097-479e-904a-13dd7198c1dd',
    )
    redis_data = GenreResponse.parse_raw(redis_data)

    assert redis_data == should_be


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает все жанры из ES""",
            {
                'method': '/genres/',
            },
            ALL_GENRES,
        ],
    ]

)
async def test_get_genres_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_request
):
    response = await make_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_get_genres_with_redis_handler(
        es_client, redis_client, make_request
):
    # кидаем запрос и ждем что ответ окажется в redis
    await make_request(method='/genres/')
    redis_data = await redis_client.get(
        key=f'{SERVICE_URL}{test_settings.api_v1_prefix}/genres',
    )

    redis_data = [GenreResponse.parse_raw(ch) for ch in json.loads(redis_data)]

    assert redis_data == ALL_GENRES
