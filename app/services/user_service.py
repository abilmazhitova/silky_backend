from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import User


class UserService:

    @staticmethod
    async def get_or_create_user(session: AsyncSession, telegram_id: str):
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            return user

        # Создаём нового пользователя
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def link_app_user(session: AsyncSession, telegram_id: str, app_user_id: str):
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            # Если Telegram юзера нет — создаём
            user = User(
                telegram_id=telegram_id,
                app_user_id=app_user_id
            )
            session.add(user)
        else:
            user.app_user_id = app_user_id

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user(session: AsyncSession, telegram_id: str):
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
