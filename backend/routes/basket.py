from fastapi import APIRouter, Body
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from backend.models.basket import BasketSchema, UpdateBasket, AddToBasketSchema
from backend.db.basket import (
    add_basket,
    add_product_to_basket,
    delete_basket,
    update_basket,
    retrieve_basket,
    retrieve_baskets,
)
from backend.db.mongodb import baskets_collection, products_collection

from backend.utils import ResponseModel, ErrorResponseModel


router = APIRouter()


@router.get("/", response_description="Get all baskets")
async def get_baskets():
    baskets = await retrieve_baskets()
    if baskets:
        return ResponseModel(baskets, "baskets data retrieved successfully")
    return ResponseModel(baskets, "Empty list returned")


@router.get("/{id}", response_description="Get basket data")
async def get_basket_data(id):
    basket = await retrieve_basket(id)
    if basket:
        return ResponseModel(basket, "basket data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "basket doesn't exist.")


@router.post("/", response_description="basket data added into the database")
async def add_basket_data(basket: BasketSchema = Body(...)):
    basket = jsonable_encoder(basket)
    new_basket = await add_basket(basket)
    print(new_basket)
    return ResponseModel(new_basket, "basket added successfully.")


@router.post("/{id}", response_description="basket data added into the database")
async def add_new_product_to_basket(id, basket: AddToBasketSchema = Body(...)):
    basket = jsonable_encoder(basket)
    new_basket = await add_product_to_basket(basket, id)
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
async def update_basket_data(id: str, req: UpdateBasket = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_basket = await update_basket(id, req)
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
async def delete_basket_data(id: str):
    deleted_basket = await delete_basket(id)
    if deleted_basket:
        return ResponseModel(
            "basket with ID: {} removed".format(id), "basket deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "basket with id {0} doesn't exist".format(id)
    )
