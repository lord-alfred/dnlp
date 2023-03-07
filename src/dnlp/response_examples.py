from typing import Any

from pydantic import BaseModel


class Error400(BaseModel):
    error: str


def generate_responses(response_200: Any, content_type_200: str = 'application/json') -> dict:
    return {
        200: {
            'description': 'Успешное выполнение запроса',
            'content': {
                content_type_200: {
                    'example': response_200,
                },
            },
        },
        400: {
            'description': 'Некорректный запрос',
            'model': Error400,
        },
    }


detect_200 = [
    {
        "confidence": 0.25515657663345337,
        "code": "en",
        "name": "English",
        "family": "Indo-European",
        "endonym": "English",
        "iso639-1": "en",
        "iso639-2/T": "eng",
        "iso639-2/B": "eng",
        "iso639-3": "eng"
    },
    {
        "confidence": 0.1489272117614746,
        "code": "de",
        "name": "German",
        "family": "Indo-European",
        "endonym": "Deutsch",
        "iso639-1": "de",
        "iso639-2/T": "deu",
        "iso639-2/B": "ger",
        "iso639-3": "deu"
    },
    {
        "confidence": 0.04044952988624573,
        "code": "pt",
        "name": "Portuguese",
        "family": "Indo-European",
        "endonym": "Português",
        "iso639-1": "pt",
        "iso639-2/T": "por",
        "iso639-2/B": "por",
        "iso639-3": "por"
    }
]

tokenize_200 = [
    'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
    ('Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" '
     '(The Extremes of Good and Evil) by mr. Cicero.'),
    'The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.',
]

extract_200 = 'test this is test'

deduplicate_200 = [
    "2 sentence",
    "Another sentence",
]


detect_responses = generate_responses(detect_200)
tokenize_responses = generate_responses(tokenize_200)
extract_responses = generate_responses(extract_200, 'text/plain')
deduplicate_responses = generate_responses(deduplicate_200)
