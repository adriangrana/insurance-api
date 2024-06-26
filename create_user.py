from app.infrastructure.database.mongo_user_repository import UserServiceAdapter
from app.application.auth_service import AuthService
from app.infrastructure.database.mongodb import db

import asyncio

async def main():
    await db.connect()
    adapter = UserServiceAdapter()
    auth_service = AuthService(adapter)

    user_document = {
        "username": "admin",
        "email": "adriangrana@gmail.com",
        "hashed_password": auth_service.get_password_hash("123"),
        "disabled": False,
        "roles": ["admin", "users"]
    }

    await adapter.create_user(user_document)
    print("Usuario agregado con éxito.")
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())
