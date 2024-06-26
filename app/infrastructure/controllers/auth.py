from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from app.application.auth_service import ACCESS_TOKEN_EXPIRE_MINUTES, AuthService
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.mongo_user_repository import UserServiceAdapter
from app.infrastructure.database.mongodb import db

router = APIRouter()
# Configuración de HTTPBearer
security = HTTPBearer()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class TokenData(BaseModel):
	username: Optional[str] = None

def get_user_repo():
	return UserServiceAdapter()

def get_auth_service():
	return AuthService(get_user_repo())

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
	user = await auth_service.authenticate_user(form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = auth_service.create_access_token(
		data={"sub": user.username, "roles": user.roles}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), user_repo: UserRepository = Depends(get_user_repo)):
	token = credentials.credentials
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		roles: list = payload.get("roles", [])
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except JWTError:
		raise credentials_exception
	user = await user_repo.find_user_by_username(username=token_data.username)
	if user is None:
		raise credentials_exception
	user.roles = roles
	return user
