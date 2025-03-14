from fastapi import APIRouter
from api.v1.endpoints.users import router as users_router
from api.v1.endpoints.brands import router as brands_router
from api.v1.endpoints.categories import router as categories_router
from api.v1.endpoints.products import router as products_router
from api.v1.endpoints.orders import router as orders_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(brands_router, prefix="/brands", tags=["brands"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])