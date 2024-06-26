from pydantic import BaseModel

class Policy(BaseModel):
  id: str
  amount_insured: float
  email: str
  inception_date: str
  installment_payment: bool
  client_id: str