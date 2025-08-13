from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError

from core.deps import CurrentUser
from model.user import User
from schemas.user import User as UserSchema
from schemas.user import UserCreate, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[str])
async def read_users(
    current_user: CurrentUser
) -> List[UserSchema]:
    """
    获取用户列表
    """
    users = User.all()
    return await [user.username for user in users]

@router.post("/", response_model=UserSchema)
async def create_user(
    user_in: UserCreate
) -> UserSchema:
    """
    创建新用户
    """
    try:
        user = await User.create(
            username=user_in.username,
            email=user_in.email,
            hashed_password=""  # 临时值，将在set_password中更新
        )
        await user.set_password(user_in.password)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists"
        )

@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: CurrentUser
) -> UserSchema:
    """
    获取当前用户信息
    """
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    user_in: UserUpdate,
    current_user: CurrentUser
) -> UserSchema:
    """
    更新当前用户信息
    """
    if user_in.username:
        current_user.username = user_in.username
    if user_in.email:
        current_user.email = user_in.email
    if user_in.password:
        await current_user.set_password(user_in.password)
    else:
        await current_user.save()
    return current_user