from fastapi import APIRouter

from dewy.chunk.router import router as chunks_router
from dewy.collection.router import router as collections_router
from dewy.document.router import router as documents_router

api_router = APIRouter(prefix="/api")

api_router.include_router(collections_router)
api_router.include_router(documents_router)
api_router.include_router(chunks_router)
