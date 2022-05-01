from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = config("MONGO_DETAILS")


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_db_client() -> AsyncIOMotorClient:
    return db.client


async def connect_db():
    db.client = AsyncIOMotorClient(MONGO_DETAILS)


async def close_mongo_connection():
    db.client.close()
