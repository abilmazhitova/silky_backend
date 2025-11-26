from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base

# ---------- User ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, index=True)
    app_user_id = Column(String, nullable=True)

    favorites = relationship("FavoriteItem", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")


# ---------- Cart ----------
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(String)
    product_title = Column(String)
    product_image = Column(String)
    price_kzt = Column(Float)
    quantity = Column(Integer, default=1)
    selected_color = Column(String, nullable=True)
    selected_size = Column(String, nullable=True)

    user = relationship("User", back_populates="cart_items")


# ---------- Favorites ----------
class FavoriteItem(Base):
    __tablename__ = "favorite_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(String)
    product_title = Column(String)
    product_image = Column(String)
    price_kzt = Column(Float)

    user = relationship("User", back_populates="favorites")


# ---------- Product Cache (для WebView) ----------
class ProductCache(Base):
    __tablename__ = "product_cache"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True)
    title = Column(String)
    image = Column(String)
    price_kzt = Column(Float)
    raw_json = Column(Text)  # оригинальный JSON из 1688
