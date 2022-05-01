from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from backend.db.mongodb import get_db_client
from backend.helpers.user_helper import admin_collection_helper
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from backend.auth.jwt import signJWT
from backend.db.user import add_admin
from backend.models.admin import AdminModel


router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(
    admin_credentials: HTTPBasicCredentials = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    # NEW CODE
    admin_user = await admin_collection_helper(client).find_one(
        {"email": admin_credentials.username}, {"_id": 0}
    )
    if admin_user:
        password = hash_helper.verify(
            admin_credentials.password, admin_user["password"]
        )
        if password:
            return signJWT(admin_credentials.username)

        return "Incorrect email or password"

    return "Incorrect email or password"


@router.post("/")
async def admin_signup(
    admin: AdminModel = Body(...),
    client: AsyncIOMotorClient = Depends(get_db_client),
):
    admin_exists = await admin_collection_helper(client).find_one(
        {"email": admin.email}, {"_id": 0}
    )
    if admin_exists:
        return "Email already exists"

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(jsonable_encoder(admin))
    return new_admin
