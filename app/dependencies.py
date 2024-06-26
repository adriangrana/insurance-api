from typing import List
from fastapi import Depends, HTTPException, status
from app.domain.models.user import User
from app.infrastructure.controllers.auth import get_current_user

def role_required(required_roles: List[str]):
	def role_dependency(user: User = Depends(get_current_user)):
		if not all(role in user.roles for role in required_roles):
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Operation not permitted",
			)
		return user
	return role_dependency