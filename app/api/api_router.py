from fastapi.routing import APIRouter
from app.api.endpoints import products,users

router=APIRouter()


router.include_router(products.router,prefix="/products",tags=["products"])
router.include_router(users.router,prefix="/users",tags=["users"])