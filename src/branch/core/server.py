from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)
from pydantic_settings import (
    BaseSettings,
)
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # print("TODO#on_startup ...")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/docs",
        title=app.title + " - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get("/probes/live")
async def probes_live():
    return {"now": datetime.now()}


class ServerSettings(BaseSettings):
    host: str
    port: int
    ui_port: int
    log_level: str


def run(settings: ServerSettings):
    uvicorn.run(
        app, host=settings.host, port=settings.port, log_level=settings.log_level
    )
