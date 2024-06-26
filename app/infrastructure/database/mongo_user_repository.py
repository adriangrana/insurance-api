from app.infrastructure.config import Settings
from app.domain.models.user import User
from app.infrastructure.database.mongodb import db

class UserServiceAdapter:
	def __init__(self):
		print(Settings.mongodb_db)
		if (db.client):
			self.init_collection()

	def init_collection(self):
		self.collection = db.client[Settings.mongodb_db]["users"]

	async def find_user_by_username(self, username: str) -> User:
		if not hasattr(self, "collection"):
			self.init_collection()
		user_data = await self.collection.find_one({"username": username})
		if user_data:
			return User(**user_data)
		return None

	async def create_user(self, user: User):
		if not hasattr(self, "collection"):
			self.init_collection()
		await self.collection.insert_one(user.dict())
