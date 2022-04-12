from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from backend.db.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from backend.models.user import (
    UserSchema,
    UserOut,
)
from backend.db.mongodb import user_collection
from backend.utils import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.get("/", response_description="Get all users")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="Get User data")
async def get_user_data(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user_exists = await user_collection.find_one({"email": user.email})
    if user_exists:
        return "user already exists"
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.put("/{id}")
async def update_user_data(id: str, req: UserOut = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the User data.",
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
