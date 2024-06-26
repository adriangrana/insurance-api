# Insurance API
![coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![GitHub issues](https://img.shields.io/github/issues/adriangrana/insurance-api)

## Description

This project is a Web API that manages insurance policies and company clients. It is built using the FastAPI framework and follows the hexagonal architecture pattern.

## Desitions
- Create a mongo db to store users and create a oauth system
- Take the registered users in mongodb for the authorization because the clients in the https://run.mocky.io/v3/d70ddb79-89af-4959-8fc1-f24c2ca9839c only have a role per users, and some endpoints require 2 roles to get access. For that reason the users store in mongodb has a list of roles and a hashed password to make the authentication and return a jwt token.
- Create a create_user.py to store users in db.
- Create a clean.sh script to clean all auto generated files.
- Create a dockerfile to deploy the api if is needed. To test this in local should put the mongo docker container in the same network that insurance-api docker container to ensure the communicaction between them.

## Endpoints
- `POST /auth/token`: Login with an exist user in mongo db and retun a jwt token require by all others endpoints for the authorization.
- `GET /users/{user_id}`: Get user data filtered by user id (accessible by users with role "users" and "admin").
- `GET /users/name/{user_name}`: Get user data filtered by user name (accessible by users with role "users" and "admin").
- `GET /policies/user/{user_name}`: Get the list of policies linked to a user name (accessible by users with role "admin").
- `GET /users/policy/{policy_id}`: Get the user linked to a policy number (accessible by users with role "admin").

## Folder Structure

```sh
app/
├── application/
│   ├── services/
│   │   └── auth_service.py
│   │   └── client_service.py
│   │   └── policy_service.py
├── domain/
│   ├── models/
│   │   └── client.py
│   │   └── policy.py
│   │   └── user.py
│   ├── repositories/
│   │   └── client_repository.py
│   │   └── policy_repository.py
│   │   └── user_repository.py
│   └── exceptions.py
├── infrastructure/
│   ├── controllers/
│   │   └── insurance.py
│   │   └── auth.py
│   ├── database/
│   │   ├── mongodb.py
│   │   └── mongo_user_repository.py
│   ├── http/
│   │   ├── http_client_repository.py
│   │   └── http_policy_repository.py
│   └── config.py
├── dependencies.py
└── main.py
test/
├── conftest.py
├── test_auth.py
├── test_insurance.py
├── test_auth_service.py
├── test_client_service.py
├── test_policy_service.py
├── test_client_service.py
├── test_http_client_repository.py
├── test_http_policy_repository.py
└── test_mongo_user_repository.py

```
## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/adriangrana/insurance-api.git
    cd insurance-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create mongodb:
    ```sh
     run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_DATABASE=insurance_db mongo
    ```

5. Create first user

    ```sh
    python create_user.py
    ```
    NOTE: inside of **create_user.py** script a default user document is defined, the user values could be changed, the main objectives of this user is to login in  **POST: /auth/token** to get a jwt token required by the others endpoints.


6. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```

7. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Testing

To run the tests, use the following command:
```sh
pytest -v
```


### requirements.txt

- fastapi
- uvicorn
- httpx
- pydantic
- pytest
- pytest-cov
- pytest-mock
- pytest-asyncio
- python-jose
- pytest_httpx
- motor
- passlib[bcrypt]
- bcrypt==3.2.0

