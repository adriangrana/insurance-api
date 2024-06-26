from app.domain.models.user import User
from app.infrastructure.config import Settings
from app.infrastructure.database.mongodb import db

class UserServiceAdapter:
	def __init__(self, mydb=db):
		self.mydb = mydb
		self.init_collection()

	def init_collection(self):
		if self.mydb.client:
			self.collection = self.mydb.client[Settings.mongodb_db]["users"]

	async def find_user_by_username(self, username: str) -> User:
		user_data = await self.collection.find_one({"username": username})
		if user_data:
			return User(**user_data)
		return None

	async def create_user(self, user: User):
		await self.collection.insert_one(user)
