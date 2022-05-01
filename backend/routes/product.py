from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi_redis_cache import cache

from backend.models.product import ProductSchema
from backend.db.product import (
    add_product,
    delete_product,
    update_product,
    retrieve_product,
    retrieve_products,
)
from backend.db.mongodb import products_collection
from backend.utils import ResponseModel, ErrorResponseModel


router = APIRouter()


@router.get("/", response_description="Get all products")
@cache(expire=5)
async def get_products():
    products = await retrieve_products()
    if products:
        return ResponseModel(products, "products data retrieved successfully")
    return ResponseModel(products, "Empty list returned")


@router.get("/{id}", response_description="Get product data")
async def get_product_data(id):
    product = await retrieve_product(id)
    if product:
        return ResponseModel(product, "product data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "product doesn't exist.")


@router.post("/", response_description="product data added into the database")
async def add_product_data(product: ProductSchema = Body(...)):
    product_exists = await products_collection.find_one({"name": product.name})
    if product_exists:
        return "product already exists"
    product = jsonable_encoder(product)
    new_product = await add_product(product)
    return ResponseModel(new_product, "product added successfully.")


@router.put("/{id}")
async def update_product_data(id: str, req: ProductSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_product = await update_product(id, req)
    if updated_product:
        return ResponseModel(
            "product with ID: {} name update is successful".format(id),
            "product name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the product data.",
    )


@router.delete("/{id}", response_description="product data deleted from the database")
async def delete_product_data(id: str):
    deleted_product = await delete_product(id)
    if deleted_product:
        return ResponseModel(
            "product with ID: {} removed".format(id), "product deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "product with id {0} doesn't exist".format(id)
    )
