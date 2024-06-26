from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from app.domain.models.client import Client
from app.domain.models.policy import Policy
from app.application.client_service import ClientService
from app.application.policy_service import PolicyService
from app.infrastructure.http_client_repository import ClientServiceAdapter
from app.infrastructure.http_policy_repository import PolicyServiceAdapter
from app.domain.exceptions import UserNotFoundException, PolicyNotFoundException

app = FastAPI(
    title="Insurance Management API",
    description="API for managing insurance policies and company clients",
    version="1.0.0"
)

def get_client_service():
    client_adapter = ClientServiceAdapter()
    return ClientService(client_adapter)

def get_policy_service():
    client_adapter = ClientServiceAdapter()
    policy_adapter = PolicyServiceAdapter()
    return PolicyService(policy_adapter, client_adapter)

@app.get("/users/{user_id}", response_model=Client, tags=["Users"])
async def get_user_by_id(user_id: str, client_service: ClientService = Depends(get_client_service)):
    try:
        return await client_service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/users/name/{user_name}", response_model=Client, tags=["Users"])
async def get_user_by_name(user_name: str, client_service: ClientService = Depends(get_client_service)):
    try:
        return await client_service.get_user_by_name(user_name)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/policies/user/{user_name}", response_model=List[Policy], tags=["Policies"])
async def get_policies_by_username(user_name: str, policy_service: PolicyService = Depends(get_policy_service)):
    try:
        return await policy_service.get_policies_by_username(user_name)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/users/policy/{policy_id}", response_model=Client, tags=["Policies"])
async def get_user_by_policy_number(policy_id: str, policy_service: PolicyService = Depends(get_policy_service)):
    try:
        return await policy_service.get_user_by_policy_number(policy_id)
    except PolicyNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
