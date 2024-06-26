from pydantic import BaseModel

class Policy(BaseModel):
  id: str
  amountInsured: float
  email: str
  inceptionDate: str
  installmentPayment: bool
  clientId: str