from enum import Enum


class ElasticIndexes(Enum):
    MOVIES = 'movies'
    PERSONS = 'persons'
    GENRES = 'genres'


class NestedObjectsFilter(Enum):
    GENRES = 'genres'
