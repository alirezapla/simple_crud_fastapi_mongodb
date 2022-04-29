from fastapi import FastAPI, Depends

from backend.auth.jwt import JWTBearer
from backend.routes.user import router as UserRouter
from backend.routes.admin import router as AdminRouter
from backend.routes.basket import router as BasketRouter
from backend.routes.product import router as ProductRouter

app = FastAPI()

token_listener = JWTBearer()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(
    UserRouter,
    tags=["Users"],
    prefix="/user",
    # dependencies=[Depends(token_listener)],
)
app.include_router(
    BasketRouter,
    tags=["Baskets"],
    prefix="/basket",
    # dependencies=[Depends(token_listener)],
)
app.include_router(
    ProductRouter,
    tags=["Products"],
    prefix="/product",
    # dependencies=[Depends(token_listener)],
)
