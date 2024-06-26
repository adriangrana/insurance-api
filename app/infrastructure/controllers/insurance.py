from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from contextlib import asynccontextmanager
from app.application.client_service import ClientService
from app.application.policy_service import PolicyService
from app.domain.exceptions import PolicyNotFoundException, UserNotFoundException
from app.domain.models.client import Client
from app.domain.models.policy import Policy
from app.domain.models.user import User
from app.infrastructure.database.mongodb import db
from app.dependencies import role_required
from .auth import router as auth_router
from app.infrastructure.http.http_client_repository import ClientServiceAdapter
from app.infrastructure.http.http_policy_repository import PolicyServiceAdapter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()

app = FastAPI(
    title="Insurance Management API",
    description="API for managing insurance policies and company clients",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

def get_client_service():
    client_adapter = ClientServiceAdapter()
    return ClientService(client_adapter)

def get_policy_service():
    client_adapter = ClientServiceAdapter()
    policy_adapter = PolicyServiceAdapter()
    return PolicyService(policy_adapter, client_adapter)

@app.get("/users/{user_id}", response_model=Client, tags=["Users"])
async def get_user_by_id(user_id: str, client_service: ClientService = Depends(get_client_service), user: User = Depends(role_required(["users", "admin"]))):
    try:
        return await client_service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/users/name/{user_name}", response_model=Client, tags=["Users"])
async def get_user_by_name(user_name: str, client_service: ClientService = Depends(get_client_service), user: User = Depends(role_required(["users", "admin"]))):
    try:
        return await client_service.get_user_by_name(user_name)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/policies/user/{user_name}", response_model=List[Policy], tags=["Policies"])
async def get_policies_by_username(user_name: str, policy_service: PolicyService = Depends(get_policy_service), user: User = Depends(role_required(["admin"]))):
    try:
        return await policy_service.get_policies_by_username(user_name)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/users/policy/{policy_id}", response_model=Client, tags=["Policies"])
async def get_user_by_policy_number(policy_id: str, policy_service: PolicyService = Depends(get_policy_service), user: User = Depends(role_required(["admin"]))):
    try:
        return await policy_service.get_user_by_policy_number(policy_id)
    except PolicyNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
