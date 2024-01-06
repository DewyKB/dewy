from fastapi import APIRouter

from app.unstructured.router import router as unstructured_router

api_router = APIRouter(prefix="/api")

api_router.include_router(unstructured_router)
