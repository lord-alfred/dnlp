import asyncio
from functools import wraps
from typing import List

from Levenshtein import ratio as levenshtein_ratio
from aiohttp.web import json_response


def sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))
    return wrapper


def abort(error_text: str):
    return json_response(
        {
            'error': error_text,
        },
        status=400,
    )


def deduplicate_sentences(sentences: List[str], threshold: float) -> List[str]:
    result = []

    for i in range(len(sentences)):
        is_duplicated = False

        for j in range(i + 1, len(sentences)):
            compared_ratio = levenshtein_ratio(sentences[i], sentences[j])

            if compared_ratio > threshold:
                is_duplicated = True
                break

        if not is_duplicated:
            result.append(sentences[i])

    return result
