from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from backend.db.mongodb import get_db_client
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from backend.db.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
    check_user_exists,
)
from backend.models.user import UserOut, UserSchema


router = APIRouter()


@router.get("/", response_description="Get all users")
async def get_users(client: AsyncIOMotorClient = Depends(get_db_client)):
    users = await retrieve_users(client)
    if users:
        return JSONResponse(
            status_code=201,
            content={"user": users, "message": "Users data retrieved successfully"},
        )
    return JSONResponse(
        status_code=204, content={"user": users, "message": "Empty list returned"}
    )


@router.get("/{id}", response_description="Get User data")
async def get_user_data(id, client: AsyncIOMotorClient = Depends(get_db_client)):
    user = await retrieve_user(id, client)
    if user:
        return JSONResponse(
            status_code=201,
            content={"user": user, "message": "Users data retrieved successfully"},
        )
    return JSONResponse(status_code=404, content="User doesn't exist.")


@router.post("/", response_description="User data added into the database")
async def add_user_data(
    user: UserSchema = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    user_exists = await check_user_exists(client, user)
    if user_exists:
        return JSONResponse(status_code=409, content="user already exists")
    user = jsonable_encoder(user)
    new_user = await add_user(client, user)
    return JSONResponse(
        status_code=201,
        content={"user": new_user, "message": "User added successfully."},
    )


@router.put("/{id}")
async def update_user_data(
    id: str,
    req: UserOut = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req, client)
    if updated_user:
        return JSONResponse(
            status_code=201,
            content="User with ID: {} name update is successful".format(id),
        )

    return JSONResponse(
        status_code=404, content="There was an error updating the User data."
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(
    id: str, client: AsyncIOMotorClient = Depends(get_db_client)
):
    deleted_user = await delete_user(id, client)
    if deleted_user:
        return JSONResponse(
            status_code=200, content="User with ID: {} removed".format(id)
        )
    return JSONResponse(
        status_code=404, content="User with id {0} doesn't exist".format(id)
    )
