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
        basket = basket_helper(basket)
        baskets.append(basket)
    return baskets


async def add_basket(basket_data: dict) -> dict:
    product = await products_collection.find_one(
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
        basket = await baskets_collection.insert_one(basket_data)
        print("***", basket.inserted_id)
        return basket_helper(basket_data)
    return False


async def add_product_to_basket(basket_data: dict, id: str) -> dict:
    product = await products_collection.find_one(
        {"_id": ObjectId(basket_data["item_id_quantity"]["item_id"])}
    )
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
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
        await baskets_collection.update_one({"_id": ObjectId(id)}, {"$set": basket})
        return basket_helper(basket)
    return False


async def retrieve_basket(id: str) -> dict:
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
    if basket:
        return basket_helper(basket)


async def update_basket(id: str, basket_data: dict):
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
    if basket:
        basket["items"] = {
            "name": basket_data["name"],
            "item_count": basket_data["items_uid_count"]["quantity"],
            "price": basket_data["item_id_quantity"]["quantity"]
            * (basket["price"] / basket["items_uid_count"]["quantity"]),
        }
        updated_basket = await baskets_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": basket}
        )
        if updated_basket:
            return basket_helper(basket)

        return False
    return False


async def delete_basket(id: str):
    basket = await baskets_collection.find_one({"_id": ObjectId(id)})
    if basket:
        await baskets_collection.delete_one({"_id": ObjectId(id)})
        return True
