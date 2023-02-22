import os
from functools import lru_cache
from typing import Any

from Levenshtein import ratio as levenshtein_ratio
from fasttext import load_model as fasttext_load
from nltk.data import load as nltk_load
from trafilatura.settings import use_config as trafilatura_use_config

from languages import FASTTEXT_LANGUAGES


def remap_fasttext_prediction(prediction: list[dict]) -> list[dict]:
    """Перегруппировка результата ответа fastText в json-совместимый ответ пользователю"""

    result = []
    if not prediction[0]:
        return result

    for index in range(len(prediction[0])):
        lang = prediction[0][index].replace('__label__', '')

        result.append({
            'confidence': prediction[1][index],
            'code': lang,
            'name': FASTTEXT_LANGUAGES[lang][1],
            'family': FASTTEXT_LANGUAGES[lang][0],
            'endonym': FASTTEXT_LANGUAGES[lang][2],
            'iso639-1': FASTTEXT_LANGUAGES[lang][3],
            'iso639-2/T': FASTTEXT_LANGUAGES[lang][4],
            'iso639-2/B': FASTTEXT_LANGUAGES[lang][5],
            'iso639-3': FASTTEXT_LANGUAGES[lang][6],
        })

    return sorted(result, key=lambda d: d['confidence'], reverse=True)


@lru_cache
def get_nltk(language: str) -> Any:
    """Загрузка nltk для токенизации с использованием кэширования токенайзера под каждый язык."""

    return nltk_load(f'tokenizers/punkt/{language}.pickle')


def get_fasttext_model() -> Any:
    """Загрузка модели fastText"""

    model_path = os.environ.get('MODEL_PATH', None)
    if not model_path or not os.path.exists(model_path):
        raise RuntimeError('Environment variable "MODEL_PATH" empty or file not exists!')

    return fasttext_load(model_path)


def get_trafilatura_config() -> Any:
    """Создание конфига trafilatura для отключения сигналов."""

    config = trafilatura_use_config()
    config.set('DEFAULT', 'EXTRACTION_TIMEOUT', '0')

    return config


def deduplicate_sentences(sentences: list[str], threshold: float) -> list[str]:
    """Удаление нечётких дублей строк"""

    result = []

    for i in range(len(sentences)):
        is_duplicated = False

        for j in range(i + 1, len(sentences)):
            computed_ratio = levenshtein_ratio(sentences[i], sentences[j])

            if computed_ratio > threshold:
                is_duplicated = True
                break

        if not is_duplicated:
            result.append(sentences[i])

    return result
