from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.db.models import CartItem, User
from app.core.config import settings
import httpx




async def fetch_product_detail(offer_id: str):
    url = f"{settings.API_1688_URL}/marketplaces/1688/product/detail/"
    params = {
        "offer_id": offer_id,
        "country": "ru",
        "skip_cache": "false"
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        return data["data"]["result"]["result"]




async def add_to_cart(
    session: AsyncSession,
    telegram_id: str,
    offer_id: str,
    sku_id: str,
):
    
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.flush()

    
    product = await fetch_product_detail(offer_id)

    
    sku = next((s for s in product["productSkuInfos"] if str(s["skuId"]) == str(sku_id)), None)
    if not sku:
        raise ValueError("Такого SKU нет у товара")

    
    title = product["subjectTrans"]
    base_image = product["productImage"]["images"][0]

    
    sku_image = sku["skuAttributes"][0].get("skuImageUrl", base_image)

    
    selected_color = None
    selected_size = None

    for attr in sku["skuAttributes"]:
        if attr["attributeNameTrans"] == "цвет":
            selected_color = attr["valueTrans"]
        if attr["attributeNameTrans"] in ("емкость", "размер", "size"):
            selected_size = attr["valueTrans"]

  
    price_kzt = float(sku["fenxiaoPriceInfo"]["onePiecePrice"]) * 76.5 * 1.3  

   
    result = await session.execute(
        select(CartItem).where(
            CartItem.user_id == user.id,
            CartItem.product_id == str(offer_id),
            CartItem.selected_color == selected_color,
            CartItem.selected_size == selected_size,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.quantity += 1
    else:
        item = CartItem(
            user_id=user.id,
            product_id=str(offer_id),
            product_title=title,
            product_image=sku_image,
            price_kzt=price_kzt,
            quantity=1,
            selected_color=selected_color,
            selected_size=selected_size,
        )
        session.add(item)

    await session.commit()
    return {"status": "ok"}




async def get_cart(session: AsyncSession, telegram_id: str):
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return []

    result = await session.execute(
        select(CartItem).where(CartItem.user_id == user.id)
    )
    items = result.scalars().all()
    return items




async def remove_item(session: AsyncSession, telegram_id: str, item_id: int):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        return False

    await session.execute(
        delete(CartItem).where(CartItem.id == item_id, CartItem.user_id == user.id)
    )
    await session.commit()
    return True




async def change_qty(session: AsyncSession, telegram_id: str, item_id: int, qty: int):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        return False

    result = await session.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        return False

    item.quantity = qty
    await session.commit()
    return True
