from .mongodb import ObjectId, baskets_collection, products_collection
from fastapi.encoders import jsonable_encoder


def basket_helper(basket) -> dict:
    return {
        "id": str(basket["_id"]),
        "items": basket["items"],
        "updated_at": basket["updated_at"],
        "created_at": basket["created_at"],
        "status": basket["status"],
    }


async def retrieve_baskets():
    baskets = []
    async for basket in baskets_collection.find():
        baskets.append(basket_helper(basket))
    return baskets


async def add_basket(basket_data: dict) -> dict:
    products = []
    for i in range(len(basket_data["items_uid_count"])):
        product = await products_collection.find_one(
            {"uid": basket_data["items_uid_count"][i][0]}
        )
        basket_data["items"].append(
            {
                "uid": product["uid"],
                "name": product["name"],
                "_id": str(product["_id"]),
                "item_count": basket_data["items_uid_count"][i][1],
            }
        )
        products.append(product)
    basket_data["updated_at"] = None
    if len(products) > 0:
        basket = await baskets_collection.insert_one(basket_data)
        new_basket = await baskets_collection.find_one({"_id": basket.inserted_id})
        return basket_helper(new_basket)
    return False


async def retrieve_basket(id: str) -> dict:
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
    if basket:
        return basket_helper(basket)


async def update_basket(id: str, basket_data: dict):
    if len(basket_data) < 1:
        return False
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
    if basket:
        products = []
        for i in range(len(basket_data["items_uid_count"])):
            product = await products_collection.find_one(
                {"uid": basket_data["items_uid_count"][i][0]}
            )
            basket_data["items"].append(
                {
                    "uid": product["uid"],
                    "name": product["name"],
                    "_id": str(product["_id"]),
                    "item_count": basket_data["items_uid_count"][i][1],
                }
            )
            products.append(product)
    if len(products) > 0:
        updated_basket = await baskets_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": basket_data}
        )
        if updated_basket:
            return True
        return False


async def delete_basket(id: str):
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
    if basket:
        await baskets_collection.delete_one({"_id": ObjectId(id)})
        return True
