import json
from uuid import UUID

import pytest

from src.models.film_works import FilmWorkResponse
from src.models.persons import PersonResponse
from tests.functional.conftest import SERVICE_URL
from tests.functional.settings import test_settings
from tests.functional.testdata.person import (CAITLIN_FOWLER, FAKE_PERSON_SHORT_DATA, FAKE_PERSON_UUID, KEIICHI_ABE,
                                              KEIICHI_ABE_FILMS)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает из ES персону по query""",
            {
                'method': '/persons/search?query=captain&page[number]=1&page[size]=50',
            },
            [
                CAITLIN_FOWLER
            ],
        ],
        [
            """Нет подходящих - получаем пустой список""",
            {
                'method': '/persons/search?query=cassssssptain',
            },
            [],
        ],
    ]

)
async def test_search_person_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_get_request
):
    response = await make_get_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_search_person_with_redis_handler(
        es_client, redis_client, make_get_request
):
    should_be = [
        PersonResponse(
            uuid=CAITLIN_FOWLER['uuid'],
            full_name='Caitlin Fowler', roles=['actor'],
            film_ids=[UUID(f_id) for f_id in CAITLIN_FOWLER['film_ids']]
        )
    ]

    # кидаем запрос и ждем что ответ окажется в redis
    await make_get_request(method='/persons/search?query=captain')

    redis_data = await redis_client.get(
        name=f'{SERVICE_URL}{test_settings.api_v1_prefix}/persons/search?query=captain',
    )

    redis_data = [PersonResponse.parse_raw(ch) for ch in json.loads(redis_data)]

    assert redis_data == should_be


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает из ES персону по uuid""",
            {
                'method': f'/persons/{KEIICHI_ABE["uuid"]}',
            },
            KEIICHI_ABE,
        ],
        [
            """Получает из ES персону по uuid, но такого uuid у нас нет - валимся в 404""",
            {
                'method': f'/persons/{FAKE_PERSON_UUID}',
            },
            FAKE_PERSON_SHORT_DATA,
        ],
    ]

)
async def test_get_persons_by_id_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_get_request
):
    response = await make_get_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_get_persons_by_id_with_redis_handler(
        es_client, redis_client, make_get_request
):
    should_be = PersonResponse(
        uuid=KEIICHI_ABE['uuid'],
        full_name=KEIICHI_ABE['full_name'], roles=KEIICHI_ABE['roles'],
        film_ids=[UUID(f_id) for f_id in KEIICHI_ABE['film_ids']]
    )

    # кидаем запрос и ждем что ответ окажется в redis
    await make_get_request(method=f'/persons/{KEIICHI_ABE["uuid"]}')

    redis_data = await redis_client.get(
        name=f'{SERVICE_URL}{test_settings.api_v1_prefix}/persons/{KEIICHI_ABE["uuid"]}',
    )

    redis_data = PersonResponse.parse_raw(redis_data)

    assert redis_data == should_be


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает из ES фильмы по персоне""",
            {
                'method': f'/persons/{KEIICHI_ABE["uuid"]}/film',
            },
            KEIICHI_ABE_FILMS,
        ],
        [
            """Получает из ES фильмы по uuid персоны, но такого uuid у нас нет - получаем пустой список""",
            {
                'method': f'/persons/{FAKE_PERSON_UUID}/film',
            },
            [],
        ],
    ]

)
async def test_get_persons_film_works_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_get_request
):
    response = await make_get_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_get_persons_film_works_with_redis_handler(
        es_client, redis_client, make_get_request
):
    should_be = [
        FilmWorkResponse(**KEIICHI_ABE_FILMS[0])
    ]

    # кидаем запрос и ждем что ответ окажется в redis
    await make_get_request(method=f'/persons/{KEIICHI_ABE["uuid"]}/film')

    redis_data = await redis_client.get(
        name=f'{SERVICE_URL}{test_settings.api_v1_prefix}/persons/{KEIICHI_ABE["uuid"]}/film',
    )

    redis_data = [FilmWorkResponse.parse_raw(ch) for ch in json.loads(redis_data)]

    assert redis_data == should_be
