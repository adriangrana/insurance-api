from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.domain.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
	def __init__(self, user_repo: UserRepository):
		self.user_repo = user_repo

	def verify_password(self, plain_password, hashed_password):
		return pwd_context.verify(plain_password, hashed_password)

	def get_password_hash(self, password):
		return pwd_context.hash(password)

	async def authenticate_user(self, username: str, password: str):
		user = await self.user_repo.find_user_by_username(username)
		if user and self.verify_password(password, user.hashed_password):
			return user
		return False

	def create_access_token(self, data: dict, expires_delta: timedelta = None):
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=15)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
		return encoded_jwt
