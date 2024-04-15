from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from middlewares import oauth
from middlewares.config import Settings, get_settings
from middlewares.exception_handlers import request_validation_exception_handler, http_exception_handler, \
    unhandled_exception_handler
from middlewares.log_request import log_request_middleware
from models import ResponseData
from routers.system import user

app = FastAPI(root_path="/v1")

# middlewares
app.add_middleware(GZipMiddleware, minimum_size=1000)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(oauth.router)
app.include_router(user.router)


@app.get("/info", response_model=ResponseData[Settings])
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return ResponseData.success(settings)


@app.get("/healthy", response_model=ResponseData[str])
async def healthy():
    return ResponseData.success("healthy")


app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
