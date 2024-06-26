from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    disabled: Optional[bool] = None
    roles: List[str] = []
