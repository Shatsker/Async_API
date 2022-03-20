import logging

import aioredis
import elasticsearch
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films
from core import config
from core.config import APP_HOST, APP_PORT
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    # Можно заменить стандартный сериализатор на более шустрый, написанный на Rust
    default_response_class=ORJSONResponse,
)
app.include_router(
    films.router,
    prefix='/api/v1/films',
    tags=['film'],
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT),
        minsize=10,
        maxsize=20,
    )
    elastic.es = elasticsearch.AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'],
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=APP_HOST,
        port=APP_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
