from pydantic import BaseModel

class Client(BaseModel):
  id: str
  name: str
  email: str
  role: str
