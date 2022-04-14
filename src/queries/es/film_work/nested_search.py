from src.core.enums import NestedObjectsFilter


def get_nested_search_query_by_genre(genre_name: str):
    if not genre_name:
        return

    return {
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": NestedObjectsFilter.GENRES.value,
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "match": {
                                                f"{NestedObjectsFilter.GENRES.value}.id": genre_name
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }
    }
