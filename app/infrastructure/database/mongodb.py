from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.config import Settings


class Database:
	client: AsyncIOMotorClient = None
	db = None

	@classmethod
	async def connect(cls):
		cls.client = AsyncIOMotorClient(Settings.mongodb_uri)
		cls.db = cls.client[Settings.mongodb_db]
		print("Connected to MongoDB")

	@classmethod
	async def close(cls):
		cls.client.close()
		print("Closed MongoDB connection")

db = Database()
