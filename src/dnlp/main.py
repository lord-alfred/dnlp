from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import HTTPException
from handlers import router


app = FastAPI(
    title='dNLP',
    description='Сборник полезных штук из Natural Language Processing',
    contact={
        'name': 'Lord_Alfred',
        'url': 'https://t.me/Lord_Alfred',
    },
    version='1.0.0',
)


@app.exception_handler(HTTPException)
async def json_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.detail,
        },
    )


app.include_router(router)
