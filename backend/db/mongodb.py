import motor.motor_asyncio
from decouple import config
from bson.objectid import ObjectId

MONGO_DETAILS = config("MONGO_DETAILS") 

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

user_collection = database.get_collection("users_collection")
products_collection = database.get_collection('products_collection')
baskets_collection = database.get_collection('baskets_collection')
admin_collection = database.get_collection('admins')