from fastapi import APIRouter

from .endpoints import chat_router, user_router, login_router, service_router

api_router = APIRouter()
api_router.include_router(login_router, tags=["login"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(service_router, tags=["services"])