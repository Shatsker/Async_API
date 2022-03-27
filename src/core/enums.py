from enum import Enum


class ElasticIndexes(Enum):
    MOVIES = 'movies'
    PERSONS = 'persons'


class NestedObjectsFilter(Enum):
    GENRES = 'genres'
