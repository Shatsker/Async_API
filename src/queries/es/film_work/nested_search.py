from core.enums import NestedObjectsFilter


def get_nested_search_query_by_genre(genre_name: str):
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
