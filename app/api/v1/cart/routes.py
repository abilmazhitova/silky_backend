from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import CartItem, User
from app.api.v1.cart.schemas import AddToCartRequest
from app.db.session import get_session

router = APIRouter(prefix="/cart", tags=["Cart"])



async def get_or_create_user(session: AsyncSession, telegram_id: str):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()

    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user



@router.post("/add")
async def add_to_cart(
    data: AddToCartRequest,
    telegram_id: str,
    session: AsyncSession = Depends(get_session)
):
    user = await get_or_create_user(session, telegram_id)

    
    result = await session.execute(
        select(CartItem).where(
            CartItem.user_id == user.id,
            CartItem.product_id == data.product_id,
            CartItem.selected_color == data.selected_color,
            CartItem.selected_size == data.selected_size
        )
    )
    existing_item = result.scalars().first()

    if existing_item:
        existing_item.quantity += data.quantity
        await session.commit()
        return {"status": "updated", "item_id": existing_item.id}

    
    new_item = CartItem(
        user_id=user.id,
        product_id=data.product_id,
        product_title=data.product_title,
        product_image=data.product_image,
        price_kzt=data.price_kzt,
        quantity=data.quantity,
        selected_color=data.selected_color,
        selected_size=data.selected_size
    )

    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)

    return {"status": "added", "item_id": new_item.id}



@router.get("/")
async def get_cart(telegram_id: str, session: AsyncSession = Depends(get_session)):
    user = await get_or_create_user(session, telegram_id)

    result = await session.execute(
        select(CartItem).where(CartItem.user_id == user.id)
    )
    items = result.scalars().all()

    return items



@router.delete("/remove/{item_id}")
async def remove_from_cart(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CartItem).where(CartItem.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(item)
    await session.commit()

    return {"status": "deleted", "item_id": item_id}
