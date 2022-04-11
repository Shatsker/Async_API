import json
from uuid import UUID

import pytest
from functional.conftest import SERVICE_URL
from functional.settings import test_settings

from models.film_works import FilmWorkResponse
from models.persons import PersonResponse

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
                {
                    "uuid": "24de5fe8-985c-4e73-92d4-da015d4beea4",
                    "full_name": "Caitlin Fowler",
                    "roles": [
                        "actor"
                    ],
                    "film_ids": [
                        "527aaa26-776b-41b1-892a-d062955a49f6"
                    ]
                }
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
        es_client, redis_client, make_request
):
    response = await make_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_search_person_with_redis_handler(
        es_client, redis_client, make_request
):
    should_be = [
        PersonResponse(
            uuid='24de5fe8-985c-4e73-92d4-da015d4beea4',
            full_name='Caitlin Fowler', roles=['actor'],
            film_ids=[UUID('527aaa26-776b-41b1-892a-d062955a49f6')]
        )
    ]

    # кидаем запрос и ждем что ответ окажется в redis
    await make_request(method='/persons/search?query=captain')

    redis_data = await redis_client.get(
        key=f'{SERVICE_URL}{test_settings.api_v1_prefix}/persons/search?query=captain',
    )

    redis_data = [PersonResponse.parse_raw(ch) for ch in json.loads(redis_data)]

    assert redis_data == should_be


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает из ES персону по uuid""",
            {
                'method': '/persons/e65bfab5-6589-43cd-a48a-24d26b53a2be',
            },
            {
                "uuid": "e65bfab5-6589-43cd-a48a-24d26b53a2be",
                "full_name": "Keiichi Abe",
                "roles": [
                    "writer"
                ],
                "film_ids": [
                    "547147ed-d835-4c22-8c42-4a800d6f32b0"
                ]
            },
        ],
        [
            """Получает из ES персону по uuid, но такого uuid у нас нет - валимся в 404""",
            {
                'method': '/persons/e65bfab5-6666-43cd-a48a-24d26b53a2be',
            },
            {'detail': 'Person was not found'},
        ],
    ]

)
async def test_get_persons_by_id_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_request
):
    response = await make_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_get_persons_by_id_with_redis_handler(
        es_client, redis_client, make_request
):
    should_be = PersonResponse(
        uuid='e65bfab5-6589-43cd-a48a-24d26b53a2be',
        full_name='Keiichi Abe', roles=['writer'],
        film_ids=[UUID('547147ed-d835-4c22-8c42-4a800d6f32b0')]
    )

    # кидаем запрос и ждем что ответ окажется в redis
    await make_request(method='/persons/e65bfab5-6589-43cd-a48a-24d26b53a2be')

    redis_data = await redis_client.get(
        key=f'{SERVICE_URL}{test_settings.api_v1_prefix}/persons/e65bfab5-6589-43cd-a48a-24d26b53a2be',
    )

    redis_data = PersonResponse.parse_raw(redis_data)

    assert redis_data == should_be


@pytest.mark.parametrize(
    'case, inp_params, should_be',
    [
        [
            """Получает из ES фильмы по персоне""",
            {
                'method': '/persons/e65bfab5-6589-43cd-a48a-24d26b53a2be/film',
            },
            [
                {
                    "uuid": "547147ed-d835-4c22-8c42-4a800d6f32b0",
                    "title": "Star Force: Fugitive Alien II",
                    "imdb_rating": 1.9
                }
            ],
        ],
        [
            """Получает из ES фильмы по uuid персоны, но такого uuid у нас нет - получаем пустой список""",
            {
                'method': '/persons/e65bfab5-6666-43cd-a48a-24d26b53a2be/film',
            },
            [],
        ],
    ]

)
async def test_get_persons_film_works_handler(
        case, inp_params, should_be,
        es_client, redis_client, make_request
):
    response = await make_request(**inp_params)
    data = response.body

    assert data == should_be


async def test_get_persons_film_works_with_redis_handler(
        es_client, redis_client, make_request
):
    should_be = [
        FilmWorkResponse(
            uuid='547147ed-d835-4c22-8c42-4a800d6f32b0',
            title='Star Force: Fugitive Alien II',
            imdb_rating=1.9)
    ]

    # кидаем запрос и ждем что ответ окажется в redis
    await make_request(method='/persons/e65bfab5-6589-43cd-a48a-24d26b53a2be/film')

    redis_data = await redis_client.get(
        key=f'{SERVICE_URL}{test_settings.api_v1_prefix}/persons/e65bfab5-6589-43cd-a48a-24d26b53a2be/film',
    )

    redis_data = [FilmWorkResponse.parse_raw(ch) for ch in json.loads(redis_data)]
    print(redis_data)

    assert redis_data == should_be
