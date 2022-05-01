from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from backend.helpers.basket_helper import basket_collection_helper, basket_helper
from backend.helpers.product_helper import product_collection_helper, product_helper


async def retrieve_baskets(client):
    baskets = []
    async for basket in basket_collection_helper(client).find():
        baskets.append(basket_helper(basket))
    return baskets


async def add_basket(basket_data: dict, client) -> dict:
    product = await product_collection_helper(client).find_one(
        {"_id": ObjectId(basket_data["item_id_quantity"]["item_id"])}
    )
    if product:
        basket_data["items"][str(product["_id"])] = {
            "name": product["name"],
            "product_id": str(product["_id"]),
            "item_quantity": basket_data["item_id_quantity"]["quantity"],
            "price": basket_data["item_id_quantity"]["quantity"] * product["price"],
        }
        basket_data["updated_at"] = None
        basket = await basket_collection_helper(client).insert_one(basket_data)
        print("***", basket.inserted_id)
        return basket_helper(basket_data)
    return False


async def add_product_to_basket(basket_data: dict, id: str, client) -> dict:
    product = await product_collection_helper(client).find_one(
        {"_id": ObjectId(basket_data["item_id_quantity"]["item_id"])}
    )
    basket = await basket_collection_helper(client).find_one({"_id": ObjectId(id)})
    if product and basket:
        if str(product["_id"]) in basket["items"]:
            basket["items"][str(product["_id"])] = {
                "name": product["name"],
                "product_id": str(product["_id"]),
                "item_quantity": (
                    basket["items"][str(product["_id"])]["item_quantity"]
                    + basket_data["item_id_quantity"]["quantity"]
                ),
                "price": (
                    basket["items"][str(product["_id"])]["item_quantity"]
                    + basket_data["item_id_quantity"]["quantity"]
                )
                * product["price"],
            }
        else:
            basket["items"][str(product["_id"])] = {
                "name": product["name"],
                "product_id": str(product["_id"]),
                "item_quantity": basket_data["item_id_quantity"]["quantity"],
                "price": basket_data["item_id_quantity"]["quantity"] * product["price"],
            }
        await basket_collection_helper(client).update_one(
            {"_id": ObjectId(id)}, {"$set": basket}
        )
        return basket_helper(basket)
    return False


async def retrieve_basket(id: str, client) -> dict:
    basket = await basket_collection_helper(client).find_one({"_id": ObjectId(id)})
    if basket:
        return basket_helper(basket)


async def update_basket(id: str, basket_data: dict, client):
    basket = await basket_collection_helper(client).find_one({"_id": ObjectId(id)})
    if basket:
        basket["items"] = {
            "name": basket_data["name"],
            "item_count": basket_data["items_uid_count"]["quantity"],
            "price": basket_data["item_id_quantity"]["quantity"]
            * (basket["price"] / basket["items_uid_count"]["quantity"]),
        }
        updated_basket = await basket_collection_helper(client).update_one(
            {"_id": ObjectId(id)}, {"$set": basket}
        )
        if updated_basket:
            return basket_helper(basket)

        return False
    return False


async def delete_basket(id: str, client):
    basket = await basket_collection_helper(client).find_one({"_id": ObjectId(id)})
    if basket:
        await basket_collection_helper(client).delete_one({"_id": ObjectId(id)})
        return True
