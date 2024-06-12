import sys
import traceback
from typing import Union

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

from logger import logger
from models import ResponseData
from utils import BusinessException


async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    logger.debug("Our custom business_exception_handler was called")
    traceback.print_tb(exc.__traceback__)

    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path

    logger.error(
        f'{host}:{port} - "{request.method} {url}" - business exception: {exc}'
    )
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())))


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom request_validation_exception_handler was called")
    body = await request.body()
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {"errors": exc.errors(), "body": body.decode(), "query_params": query_params}
    logger.info(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.debug("Our custom http_exception_handler was called")
    logger.exception(exc)
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())), status_code=exc.status_code)


async def unhandled_exception_handler(request: Request, exc: Exception) -> Union[JSONResponse, Response]:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    )
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())), status_code=500)
