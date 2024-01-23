from fastapi import APIRouter

from app.chunks.router import router as chunks_router
from app.collections.router import router as collections_router
from app.documents.router import router as documents_router

api_router = APIRouter(prefix="/api")

api_router.include_router(collections_router)
api_router.include_router(documents_router)
api_router.include_router(chunks_router)
