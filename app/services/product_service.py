import httpx
from app.core.config import settings  # если у тебя есть settings.BACKEND_URL

BACKEND_URL = settings.BACKEND_URL


async def request_1688_details(offer_id: str):
    url = f"{BACKEND_URL}/marketplaces/1688/product/details/"
    
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params={"offer_id": offer_id})

    if r.status_code != 200:
        return None

    return r.json()
