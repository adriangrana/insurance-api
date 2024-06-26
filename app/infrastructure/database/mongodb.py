from motor.motor_asyncio import AsyncIOMotorClient
from app.infrastructure.config import settings

class MongoDB:
	client: AsyncIOMotorClient = None


db = MongoDB()
print(settings.mongodb_uri)


async def connect_to_mongo():
	print("Connecting to MongoDB")
	db.client = AsyncIOMotorClient(settings.mongodb_uri + "/"+settings.mongodb_db)
	print("Connected to MongoDB")


async def close_mongo_connection():
	db.client.close()
	print("Closed MongoDB connection")
