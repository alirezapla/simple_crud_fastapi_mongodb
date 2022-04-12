from .mongodb import ObjectId, products_collection


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "uid": int(product["uid"]),
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
    new_product = await products_collection.find_one({"_id": product.inserted_id})
    return product_helper(new_product)


async def retrieve_product(id: str) -> dict:
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)


async def update_product(id: str, data: dict):
    if len(data) < 1:
        return False
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        updated_product = await products_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_product:
            return True
        return False


async def delete_product(id: str):
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        await products_collection.delete_one({"_id": ObjectId(id)})
        return True
