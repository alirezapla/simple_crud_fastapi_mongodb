from .mongodb import ObjectId, products_collection, baskets_collection


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "description": product["description"],
    }


async def retrieve_products():
    products = []
    async for product in products_collection.find():
        products.append(product_helper(product))
    return products


async def add_product(product_data: dict) -> dict:
    product = await products_collection.insert_one(product_data)
    if product:
        return product_helper(product_data)
    return False


async def retrieve_product(id: str) -> dict:
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)


async def update_product(id: str, data: dict):
    if len(data) < 1:
        return False
    try:
        updated_product = await products_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_product:
            update_product_in_baskets = await baskets_collection.update_many(
                {"items.product_id": id},
                {"$set": {"items.name": data["name"]}},
            )
            if update_product_in_baskets:
                return True
        return False
    except:
        return False


async def delete_product(id: str):
    try:
        await products_collection.delete_one({"_id": ObjectId(id)})
        return True
    except:
        return False
