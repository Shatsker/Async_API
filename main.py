import logging

import aioredis
import elasticsearch
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT

from src.api.v1 import film_works, genres, persons
from src.core.config import settings
from src.core.logger import LOGGING
from src.db import elastic, redis

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    # Можно заменить стандартный сериализатор на более шустрый
    default_response_class=ORJSONResponse,
)

app.include_router(
    film_works.router,
    prefix='/api/v1/films',
    tags=['film'],
)

app.include_router(
    persons.router,
    prefix='/api/v1/persons',
    tags=['persons'],
)

app.include_router(
    genres.router,
    prefix='/api/v1/genres',
    tags=['genres'],
)


@app.on_event('startup')
async def startup():
    redis.redis = aioredis.from_url(
        f'redis://{settings.redis_host}',
        encoding="utf-8",
        decode_responses=True,
    )
    elastic.es = elasticsearch.AsyncElasticsearch(
        hosts=[f'{settings.elastic_host}:{settings.elastic_port}'],
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


@AuthJWT.load_config
def get_config():
    return settings


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.app_host,
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
