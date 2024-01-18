from fastapi import APIRouter

from app.collections.router import router as collections_router
from app.documents.router import router as documents_router
from app.statements.router import router as statements_router

api_router = APIRouter(prefix="/api")

api_router.include_router(collections_router)
api_router.include_router(documents_router)
api_router.include_router(statements_router)
