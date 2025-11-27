# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.search.routes import search_router
from app.api.v1.users.routes import router as users_router
from app.api.v1.favorites.routes import router as favorites_router
from app.api.v1.cart.routes import router as cart_router
from app.api.v1.product.routes import router as product_router
# from app.api.v1.product.routes import product_router

# from app.api.v1.webview.routes import webview_router


app = FastAPI(title="Silky Backend API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(search_router, prefix="/api/v1/search", tags=["Search"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(favorites_router, prefix="/api/v1/favorites", tags=["Favorites"])
# app.include_router(product_router, prefix="/api/v1/product", tags=["Product"])
app.include_router(cart_router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(product_router, prefix="/api/v1/product", tags=["Product"])
# app.include_router(webview_router, prefix="/api/v1/webview", tags=["WebView"])
