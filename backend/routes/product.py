import asyncio
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_redis_cache import cache
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from backend.db.mongodb import get_db_client
from backend.db.product import (
    add_product,
    delete_product,
    retrieve_product,
    retrieve_products,
    update_product,
    check_product_exist,
)
from backend.models.product import ProductSchema
from backend.utils import ErrorResponseModel, ResponseModel

router = APIRouter()


class Cache:
    enable = True
    data = None

    async def expire(cls):
        cls.enable = False
        await asyncio.sleep(0.7)
        cls.enable = True


c = Cache()


@router.get("/health_check/", response_description="Get all products")
async def health_check():
    # return JSONResponse(status_code=201, content={"ping": "pong"})
    return {"ping": "pong"}


@router.get("/", response_description="Get all products")
@cache(20)
async def get_products(client: AsyncIOMotorClient = Depends(get_db_client)):
    if c.enable == True:
        print("query")
        await c.expire()
        products = await retrieve_products(client)
        if products:
            c.data = products
            return JSONResponse(
                status_code=201,
                content={
                    "product": products,
                    "message": "product data retrieved successfully",
                },
            )
        return JSONResponse(
            status_code=200,
            content={"products": products, "message": "Empty list returned"},
        )
    print("cache")
    return JSONResponse(
        status_code=201,
        content={
            "product": c.data,
            "message": "product data retrieved successfully",
        },
    )


@router.get("/{id}", response_description="Get product data")
async def get_product_data(id, client: AsyncIOMotorClient = Depends(get_db_client)):
    product = await retrieve_product(id, client)
    if product:
        return JSONResponse(
            status_code=201,
            content={
                "product": product,
                "message": "product data retrieved successfully",
            },
        )
    return JSONResponse(status_code=404, content="product doesn't exist.")


@router.post("/", response_description="product data added into the database")
async def add_product_data(
    product: ProductSchema = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    product_exists = await check_product_exist(client, product)
    if product_exists:
        return JSONResponse(status_code=409, content="product already exists")
    product = jsonable_encoder(product)
    new_product = await add_product(product, client)
    return ResponseModel(new_product, "product added successfully.")


@router.put("/{id}")
async def update_product_data(
    id: str,
    req: ProductSchema = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_product = await update_product(id, req, client)
    if updated_product:
        return JSONResponse(
            status_code=201,
            content="product with ID: {} name update is successful".format(id),
        )
    return JSONResponse(
        status_code=404,
        content="There was an error updating the product data.",
    )


@router.delete("/{id}", response_description="product data deleted from the database")
async def delete_product_data(
    id: str, client: AsyncIOMotorClient = Depends(get_db_client)
):
    deleted_product = await delete_product(id, client)
    if deleted_product:

        return JSONResponse(
            status_code=200, content="product with ID: {} removed".format(id)
        )
    return JSONResponse(
        status_code=404, content="product with id {0} doesn't exist".format(id)
    )
