from bson.objectid import ObjectId
from backend.helpers.product_helper import product_helper, product_collection_helper
from backend.helpers.basket_helper import basket_collection_helper


async def check_product_exist(client, product):
    return await product_collection_helper(client).find_one({"name": product.name})


async def retrieve_products(client):
    products = []
    async for product in product_collection_helper(client).find():
        products.append(product_helper(product))
    return products


async def add_product(product_data: dict, client) -> dict:
    product = await product_collection_helper(client).insert_one(product_data)
    if product:
        return product_helper(product_data)
    return False


async def retrieve_product(id: str, client) -> dict:
    product = await product_collection_helper(client).find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)


async def update_product(id: str, data: dict, client):
    if len(data) < 1:
        return False
    try:
        updated_product = await product_collection_helper(client).update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_product:
            update_product_in_baskets = await basket_collection_helper(
                client
            ).update_many(
                {"items.product_id": id},
                {"$set": {"items.name": data["name"]}},
            )
            if update_product_in_baskets:
                return True
        return False
    except:
        return False


async def delete_product(id: str, client):
    try:
        await product_collection_helper(client).delete_one({"_id": ObjectId(id)})
        return True
    except:
        return False
