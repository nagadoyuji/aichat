from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from core.configs import settings
from .v1 import api_router as api_router_v1

api_router = APIRouter()
api_router.include_router(api_router_v1, prefix=settings.API_V1_STR)

def init_api(app: FastAPI) -> None:
    """初始化API，添加中间件和路由"""
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 在生产环境中应指定具体的源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(api_router)
    
    # 注册Tortoise ORM
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["model.user", "model.chat", "model.agent"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )