from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user(telegram_id: str, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_or_create_user(session, telegram_id)
    return {
        "status": "ok",
        "user_id": user.id,
        "telegram_id": user.telegram_id,
        "app_user_id": user.app_user_id
    }


@router.post("/link-app-user")
async def link_app_user(
    telegram_id: str,
    app_user_id: str,
    session: AsyncSession = Depends(get_session)
):
    user = await UserService.link_app_user(session, telegram_id, app_user_id)

    return {
        "status": "ok",
        "message": "Linked successfully",
        "telegram_id": user.telegram_id,
        "app_user_id": user.app_user_id
    }


@router.get("/{telegram_id}")
async def get_user(telegram_id: str, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_user(session, telegram_id)

    if not user:
        return {"status": "not_found"}

    return {
        "status": "ok",
        "user_id": user.id,
        "telegram_id": user.telegram_id,
        "app_user_id": user.app_user_id
    }


@router.patch("/set-language")
async def set_language(
    telegram_id: str,
    language_code: str,
    session: AsyncSession = Depends(get_session)
):
    user = await UserService.set_language(session, telegram_id, language_code)

    return {
        "status": "ok",
        "message": "Language updated",
        "telegram_id": telegram_id,
        "language_code": language_code
    }