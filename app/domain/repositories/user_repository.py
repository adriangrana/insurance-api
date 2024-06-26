from app.domain.models.user import User

class UserRepository:
	async def find_user_by_username(self, username: str) -> User:
		raise NotImplementedError

	async def create_user(self, user: User):
		raise NotImplementedError