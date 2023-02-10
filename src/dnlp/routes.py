from aiohttp import web

from dnlp.handlers import detect_language, extract, tokenize_sentences


routes = [
    web.post('/detect-language', detect_language),
    web.post('/tokenize-sentences', tokenize_sentences),
    web.post('/extract', extract),
]
