import pytest
from fastapi import HTTPException
from app.dependencies import role_required
from app.domain.models.user import User

def test_should_call_role_required():
  user = User(username="testuser", email="testuser@example.com", hashed_password="fakehashed", roles=["user"])
  dependency = role_required(["user"])
  assert dependency(user) == user

  with pytest.raises(HTTPException):
    dependency = role_required(["admin"])
    dependency(user)
