from fastapi import FastAPI

from app.config import app_configs
from app.routes import api_router

app = FastAPI(**app_configs)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
