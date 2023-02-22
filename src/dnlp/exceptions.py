from fastapi import HTTPException as FastAPIHTTPException


class HTTPException(FastAPIHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=400, detail=detail)
