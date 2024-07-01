from http.client import INTERNAL_SERVER_ERROR, BAD_REQUEST
from typing import Union

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from logger import logger
from models import ResponseData
from utils import BusinessException


async def log_request_exception(exc, request):
    """
    记录请求异常时发生的日志
    :param exc:
    :param request:
    :return:
    """
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    logger.exception(
        f'{host}:{port} - "{request.method} {url}": {exc.__str__()}'
    )


async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    logger.debug("Our custom business_exception_handler was called")
    await log_request_exception(exc, request)
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())), status_code=INTERNAL_SERVER_ERROR)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom request_validation_exception_handler was called")
    await log_request_exception(exc, request)
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())), status_code=BAD_REQUEST)


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.debug("Our custom http_exception_handler was called")
    await log_request_exception(exc, request)
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())), status_code=exc.status_code)


async def unhandled_exception_handler(request: Request, exc: Exception) -> Union[JSONResponse, Response]:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    logger.debug("Our custom unhandled_exception_handler was called")
    await log_request_exception(exc, request)
    return JSONResponse(jsonable_encoder(ResponseData.fail(msg=exc.__str__())), status_code=INTERNAL_SERVER_ERROR)
