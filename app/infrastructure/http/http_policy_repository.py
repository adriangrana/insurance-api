import httpx
from typing import List
from app.domain.models.policy import Policy
from app.domain.repositories.policy_repository import PolicyRepository
from app.infrastructure.config import settings

class PolicyServiceAdapter(PolicyRepository):
	async def fetch_policies(self) -> List[Policy]:
		async with httpx.AsyncClient() as client:
			response = await client.get(settings.policy_service_url)
			response.raise_for_status()
			policies_data = response.json()
			return [
				Policy(
					id=policy["id"],
					amount_insured=policy["amountInsured"],
					email=policy["email"],
					inception_date=policy["inceptionDate"],
					installment_payment=policy["installmentPayment"],
					client_id=policy["clientId"],
				)
				for policy in policies_data
			]
