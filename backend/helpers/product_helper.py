def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "description": product["description"],
    }


def product_collection_helper(client):
    return client.users.get_collection("product_collection")
