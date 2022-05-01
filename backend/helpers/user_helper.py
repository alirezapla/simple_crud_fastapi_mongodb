def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "national_id": user["national_id"],
        "password": user["password"],
    }


def admin_helper(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "fullname": admin["fullname"],
        "email": admin["email"],
    }


def user_collection_helper(client):
    return client.app.get_collection("users_collection")


def admin_collection_helper(client):
    return client.app.get_collection("admin_collection")
