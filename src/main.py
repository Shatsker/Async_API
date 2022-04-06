import logging

import aioredis
import elasticsearch
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import film_works, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis

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
    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    elastic.es = elasticsearch.AsyncElasticsearch(
        hosts=[f'{settings.elastic_host}:{settings.elastic_port}'],
    )


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await elastic.es.close()


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.app_host,
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
