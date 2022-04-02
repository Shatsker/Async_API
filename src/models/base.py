import orjson

from pydantic import BaseModel

from core.utils import orjson_dumps


class BaseModelConfig(BaseModel):
    """Базовый класс для моделей в приложении."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MixinAllowPopulation(BaseModel):

    class Config:
        allow_population_by_field_name = True
