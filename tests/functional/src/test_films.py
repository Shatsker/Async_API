import json

import pytest
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from tests.functional.conftest import SERVICE_URL
from tests.functional.settings import test_settings
from tests.functional.testdata.films import ALL_FILM_WORKS, FILM_NOT_FOUND, ONE_FILM_WORK, SEARCHED_FILM_WORKS

from src.models.film_works import FilmWorkResponse, FullFilmWorkResponse

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'case, inp_params, must_be',
    [
        [
            """Получаем все фильмы.""",
            {'method': '/films/?page[number]=1&page[size]=10&sort=imdb_rating'},
            ALL_FILM_WORKS,
        ],
        [
            """Получаем фильм из ES.""",
            {'method': '/films/5c855467-9c2b-491d-a179-c217ea543e93'},
            ONE_FILM_WORK,
        ],
        [
            """Поиск фильмов по слову 'fastapi'""",
            {'method': '/films/search/?query=fastapi'},
            SEARCHED_FILM_WORKS,
        ],
        [
            """Получаем несуществующий фильм из ES, падаем с 404.""",
            {'method': '/films/5c855467-9c2b-491d-a179-c217ea543e96'},
            FILM_NOT_FOUND,
        ]
    ]
)
async def test_film_works(
        case: str,
        inp_params: dict,
        must_be: dict,
        make_get_request,
        es_client: AsyncElasticsearch,
        redis_client: Redis,
):
    # второй запрос делаем для того, чтобы проверить, корректно ли кешируется запрос
    first_response = await make_get_request(**inp_params)
    second_response = await make_get_request(**inp_params)

    first_data = first_response.body
    second_data = second_response.body

    assert first_data == must_be
    assert second_data == must_be


@pytest.mark.parametrize(
    'case, inp_params, must_be',
    [
        [
            """Получаем все фильмы.""",
            {'method': '/films'},
            ALL_FILM_WORKS,
        ],
        [
            """Поиск фильмов по слову 'fastapi'""",
            {'method': '/films/search/?query=fastapi'},
            SEARCHED_FILM_WORKS,
        ]
    ]
)
async def test_get_films_with_redis_handler(
        case: str,
        inp_params: dict,
        must_be: dict,
        make_get_request,
        es_client: AsyncElasticsearch,
        redis_client: Redis,
):
    # кидаем запрос и ждем что ответ окажется в redis
    await make_get_request(**inp_params)

    redis_raw_data = await redis_client.get(
        name=f'{SERVICE_URL}{test_settings.api_v1_prefix}{inp_params["method"]}',
    )
    redis_data = [FilmWorkResponse.parse_raw(ch) for ch in json.loads(redis_raw_data)]

    assert redis_data == must_be


@pytest.mark.parametrize(
    'case, inp_params, must_be',
    [
        [
            """Получаем фильм из ES.""",
            {'method': '/films/5c855467-9c2b-491d-a179-c217ea543e93'},
            ONE_FILM_WORK,
        ],
    ]
)
async def test_get_one_film_work_by_id_with_redis_handler(
        case: str,
        inp_params: dict,
        must_be: dict,
        make_get_request,
        es_client: AsyncElasticsearch,
        redis_client: Redis,
):
    # кидаем запрос и ждем что ответ окажется в redis
    await make_get_request(**inp_params)

    redis_raw_data = await redis_client.get(
        name=f'{SERVICE_URL}{test_settings.api_v1_prefix}{inp_params["method"]}',
    )
    redis_data = FullFilmWorkResponse.parse_raw(redis_raw_data)

    assert redis_data == must_be
