from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from backend.db.mongodb import get_db_client
from backend.db.basket import (
    add_basket,
    add_product_to_basket,
    delete_basket,
    retrieve_basket,
    retrieve_baskets,
    update_basket,
)
from backend.models.basket import AddToBasketSchema, BasketSchema, UpdateBasket
from backend.utils import ErrorResponseModel, ResponseModel

router = APIRouter()


@router.get("/", response_description="Get all baskets")
async def get_baskets(client: AsyncIOMotorClient = Depends(get_db_client)):
    baskets = await retrieve_baskets()
    if baskets:
        return ResponseModel(baskets, "baskets data retrieved successfully")
    return ResponseModel(baskets, "Empty list returned")


@router.get("/{id}", response_description="Get basket data")
async def get_basket_data(id, client: AsyncIOMotorClient = Depends(get_db_client)):
    basket = await retrieve_basket(id, client)
    if basket:
        return ResponseModel(basket, "basket data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "basket doesn't exist.")


@router.post("/", response_description="basket data added into the database")
async def add_basket_data(
    basket: BasketSchema = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    basket = jsonable_encoder(basket)
    new_basket = await add_basket(basket, client)
    print(new_basket)
    return ResponseModel(new_basket, "basket added successfully.")


@router.post("/{id}", response_description="basket data added into the database")
async def add_new_product_to_basket(
    id,
    basket: AddToBasketSchema = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    basket = jsonable_encoder(basket)
    new_basket = await add_product_to_basket(basket, id, client)
    if new_basket:
        return JSONResponse(
            status_code=201,
            content={
                "message": "new product added to basket successfully.",
                "basket": new_basket,
            },
        )
    return JSONResponse(status_code=404, content={"message": "Basket not found"})


@router.put("/{id}")
async def update_basket_data(
    id: str,
    req: UpdateBasket = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_basket = await update_basket(id, req, client)
    if updated_basket:
        return JSONResponse(
            status_code=201,
            content={
                "message": "basket with ID: {} name update is successful".format(id),
            },
        )
    return JSONResponse(
        status_code=404,
        content={"message": "There was an error updating the basket data."},
    )


@router.delete("/{id}", response_description="basket data deleted from the database")
async def delete_basket_data(
    id: str, client: AsyncIOMotorClient = Depends(get_db_client)
):
    deleted_basket = await delete_basket(id, client)
    if deleted_basket:
        return ResponseModel(
            "basket with ID: {} removed".format(id), "basket deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "basket with id {0} doesn't exist".format(id)
    )
