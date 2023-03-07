from fastapi import APIRouter, Body, Form
from fastapi.responses import PlainTextResponse
from trafilatura.core import extract as trafilatura_extract

from exceptions import HTTPException
from helpers import (
    deduplicate_sentences,
    get_fasttext_model,
    get_nltk,
    get_trafilatura_config,
    remap_fasttext_prediction,
)
from languages import PUNKT_LANGUAGES, PunktLanguagesEnum
from preprocess import fix_bad_unicode, normalize_html, normalize_whitespace, preprocess_text
from response_examples import deduplicate_responses, detect_responses, extract_responses, tokenize_responses


router = APIRouter()

FASTTEXT_MODEL = get_fasttext_model()
TRAFILATURA_CONFIG = get_trafilatura_config()


@router.post(
    '/detect',
    summary='Определение языка текста',
    responses=detect_responses,
)
def detect(
    text: str = Form(description='Текст для определения языка'),
    count: int = Form(description='Количество результатов', default=3),
    threshold: float = Form(description='Пороговое значение', ge=0.0, le=1.0, default=0.01),
):

    # Предобработка текста (удаление ссылок, переносов строк, понижение регистра и тд).
    # Может аффектить на скорость из-за регулярок.
    # В будущем можно сделать отключение части обработчиков (после бенча на сколько это вообще проблема).
    text = preprocess_text(text)

    if not text:
        raise HTTPException(detail='Content of parameter `text` is empty after preprocessing')

    prediction = FASTTEXT_MODEL.predict(text, k=count, threshold=threshold)

    if not prediction:
        raise HTTPException(detail='Detection error')

    return remap_fasttext_prediction(prediction)


@router.post(
    '/tokenize',
    summary='Разделение текста на предложения',
    responses=tokenize_responses,
)
def tokenize(
    text: str = Form(description='Текст для разбивки на предложения'),
    lang: PunktLanguagesEnum = Form(description='Язык текста', default=PunktLanguagesEnum.en),
):

    text = fix_bad_unicode(text, normalization='NFC')
    text = normalize_whitespace(text)
    text = text.strip()

    if not text:
        raise HTTPException(detail='Content of parameter `text` is empty after preprocessing')

    nltk = get_nltk(PUNKT_LANGUAGES[lang.value])
    sentences = nltk.tokenize(text)

    if not sentences:
        raise HTTPException(detail='Tokenization error')

    return sentences


@router.post(
    '/extract',
    summary='Получение основного содержимого из html документа',
    response_class=PlainTextResponse,
    responses=extract_responses,
)
def extract(
    html: str = Form(description='Содержимое HTML-страницы, закодированное с помощью `urlencode` функции'),
):

    html = normalize_html(html)

    text = trafilatura_extract(
        html,
        favor_precision=True,
        include_comments=False,
        config=TRAFILATURA_CONFIG,
    )

    if not text:
        raise HTTPException(detail='Extraction error')

    return text


@router.post(
    '/deduplicate',
    summary='Удаление нечётких дублей приложений',
    responses=deduplicate_responses,
)
def deduplicate(
    sentences: list[str] = Body(description='Массив предложений'),
    threshold: float = Body(description='Пороговое значение', ge=0.0, le=1.0, default=0.8),
):
    dedup_sentences = deduplicate_sentences(sentences, threshold)

    if not dedup_sentences:
        raise HTTPException(detail='Deduplication error')

    return dedup_sentences
