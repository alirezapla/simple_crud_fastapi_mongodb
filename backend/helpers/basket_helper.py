def basket_helper(basket) -> dict:
    return {
        "id": str(basket["_id"]),
        "items": basket["items"],
        "updated_at": basket["updated_at"],
        "created_at": basket["created_at"],
        "status": basket["status"],
    }


def basket_collection_helper(client):
    return client.app.get_collection("basket_collection")
