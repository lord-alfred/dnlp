import asyncio
import os

from aiohttp.web import json_response
from fasttext import load_model as ft_load_model
from nltk.data import load as nltk_load

from dnlp.helpers import abort
from dnlp.languages import PUNKT_LANGUAGES
from dnlp.postprocess import remap_prediction
from dnlp.preprocess import (fix_bad_unicode, normalize_whitespace, preprocess_text)


# fastText
MODEL_PATH = os.environ.get('MODEL_PATH', None)
if not MODEL_PATH:
    raise RuntimeError('Environment variable "MODEL_PATH" empty')
FT_MODEL = ft_load_model(MODEL_PATH)

# nltk punkt
SENT_TOKENIZER = {}


async def tokenize_sentences(request):
    post_data = await request.post()
    param_text = post_data.get('text', '')

    param_text = fix_bad_unicode(param_text, normalization="NFC")
    param_text = normalize_whitespace(param_text)
    param_text = param_text.strip()

    if not param_text:
        return abort('empty "text" parameter')

    param_lang = post_data.get('lang', 'en')

    if param_lang in PUNKT_LANGUAGES.keys():
        if param_lang not in SENT_TOKENIZER.keys():
            # first tokenizer load (may be slow)
            SENT_TOKENIZER[param_lang] = nltk_load(f'tokenizers/punkt/{PUNKT_LANGUAGES[param_lang]}.pickle')
    else:
        return abort('unknown language code')

    loop = asyncio.get_event_loop()
    sentences = await loop.run_in_executor(
        executor=None,
        func=lambda: SENT_TOKENIZER[param_lang].tokenize(
            param_text
        ),
    )

    if not sentences:
        return abort('tokenization error')

    return json_response(sentences)


async def detect_language(request):
    post_data = await request.post()
    param_text = post_data.get('text', '')

    # preprocessing (normalization)
    param_text = preprocess_text(param_text)
    if not param_text:
        return abort('empty "text" parameter')

    param_count = post_data.get('count', 3)
    param_count = int(param_count)

    loop = asyncio.get_event_loop()
    prediction = await loop.run_in_executor(
        executor=None,
        func=lambda: FT_MODEL.predict(
            param_text,
            k=param_count,
            threshold=0.01
        ),
    )

    if not prediction:
        return abort('detection error')

    return json_response(
        remap_prediction(prediction)
    )
