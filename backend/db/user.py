from bson.objectid import ObjectId
from backend.helpers.user_helper import (
    user_collection_helper,
    admin_collection_helper,
    user_helper,
    admin_helper,
)


# TODO use decoratore


async def check_user_exists(user, client):
    user_collection = user_collection_helper(client)
    return await user_collection.find_one({"email": user.email})


async def add_admin(admin_data: dict, client) -> dict:
    admin_collection = admin_collection_helper(client)
    await admin_collection.insert_one(admin_data)
    return admin_helper(admin_data)


async def retrieve_users(client):
    user_collection = user_collection_helper(client)
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def add_user(user_data: dict, client) -> dict:
    user_collection = user_collection_helper(client)
    await user_collection.insert_one(user_data)
    return user_helper(user_data)


async def retrieve_user(id: str, client) -> dict:
    user_collection = user_collection_helper(client)
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def update_user(id: str, data: dict, client):
    user_collection = user_collection_helper(client)
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(id: str, client):
    user_collection = user_collection_helper(client)
    return await user_collection.delete_one({"_id": ObjectId(id)})
