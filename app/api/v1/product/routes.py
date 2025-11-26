from fastapi import APIRouter, HTTPException
from app.services.product_service import request_1688_details

router = APIRouter(prefix="/product")


@router.get("/{offer_id}")
async def get_product(offer_id: str):
    item = await request_1688_details(offer_id)

    if not item:
        raise HTTPException(status_code=404, detail="Product not found")

    return item
