from pydantic import BaseModel
from typing import Optional

class AddToCartRequest(BaseModel):
    product_id: str
    product_title: str
    product_image: str
    price_kzt: float
    selected_color: Optional[str] = None
    selected_size: Optional[str] = None
    quantity: Optional[int] = 1
