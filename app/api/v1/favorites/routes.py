from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.favorite_service import FavoriteService
from app.services.user_service import UserService
from app.db.session import get_session

router = APIRouter(prefix="/favorites", tags=["Favorites"])


# -------- Добавить в избранное --------
@router.post("/add")
async def add_favorite(
    telegram_id: str,
    product_id: str,
    title: str,
    image: str,
    price_kzt: float,
    session: AsyncSession = Depends(get_session)
):
    user = await UserService.get_or_create_user(session, telegram_id)

    item = await FavoriteService.add_to_favorites(
        session,
        user_id=user.id,
        product_id=product_id,
        title=title,
        image=image,
        price_kzt=price_kzt
    )

    return {
        "status": "ok",
        "message": "Added to favorites",
        "item": {
            "product_id": item.product_id,
            "title": item.product_title,
            "image": item.product_image,
            "price_kzt": item.price_kzt
        }
    }


# -------- Удалить из избранного --------
@router.delete("/remove")
async def remove_favorite(
    telegram_id: str,
    product_id: str,
    session: AsyncSession = Depends(get_session)
):
    user = await UserService.get_or_create_user(session, telegram_id)

    ok = await FavoriteService.remove_from_favorites(
        session,
        user_id=user.id,
        product_id=product_id
    )

    return {"status": "ok" if ok else "not_found"}


# -------- Получить список избранного --------
@router.get("/list")
async def list_favorites(
    telegram_id: str,
    session: AsyncSession = Depends(get_session)
):
    user = await UserService.get_or_create_user(session, telegram_id)

    items = await FavoriteService.list_favorites(session, user.id)

    return {
        "status": "ok",
        "count": len(items),
        "items": [
            {
                "product_id": x.product_id,
                "title": x.product_title,
                "image": x.product_image,
                "price_kzt": x.price_kzt
            }
            for x in items
        ]
    }
