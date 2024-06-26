from typing import List
from ..models.policy import Policy

class PolicyRepository:
    async def fetch_policies(self) -> List[Policy]:
        raise NotImplementedError