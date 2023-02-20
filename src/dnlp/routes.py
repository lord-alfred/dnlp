from aiohttp import web

from dnlp.handlers import deduplicate, detect, extract, tokenize


routes = [
    web.post('/detect', detect),
    web.post('/tokenize', tokenize),
    web.post('/extract', extract),
    web.post('/deduplicate', deduplicate),

    # deprecated and must be removed
    web.post('/detect-language', detect),
    web.post('/tokenize-sentences', tokenize),
]
