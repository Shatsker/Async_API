import pytest

from tests.functional.testdata.genre import ALL_GENRES

pytestmark = pytest.mark.asyncio


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
    print(data)

    assert data == should_be
    print(1)
