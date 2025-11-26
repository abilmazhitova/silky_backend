from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import FavoriteItem


class FavoriteService:

    @staticmethod
    async def add_to_favorites(
        session: AsyncSession,
        user_id: int,
        product_id: str,
        title: str,
        image: str,
        price_kzt: float,
    ):
        # Проверяем, есть ли такой товар уже в избранном
        result = await session.execute(
            select(FavoriteItem).where(
                FavoriteItem.user_id == user_id,
                FavoriteItem.product_id == product_id
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            return existing  # уже в избранном

        item = FavoriteItem(
            user_id=user_id,
            product_id=product_id,
            product_title=title,
            product_image=image,
            price_kzt=price_kzt,
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    @staticmethod
    async def remove_from_favorites(session: AsyncSession, user_id: int, product_id: str):
        result = await session.execute(
            select(FavoriteItem).where(
                FavoriteItem.user_id == user_id,
                FavoriteItem.product_id == product_id
            )
        )
        existing = result.scalar_one_or_none()

        if not existing:
            return False

        await session.delete(existing)
        await session.commit()
        return True

    @staticmethod
    async def list_favorites(session: AsyncSession, user_id: int):
        result = await session.execute(
            select(FavoriteItem).where(FavoriteItem.user_id == user_id)
        )
        return result.scalars().all()
