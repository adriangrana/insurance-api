# Insurance API

## Description

This project is a Web API that manages insurance policies and company clients. It is built using the FastAPI framework and follows the hexagonal architecture pattern.

## Endpoints

- `GET /users/{user_id}`: Get user data filtered by user id (accessible by users with role "users" and "admin").
- `GET /users/name/{user_name}`: Get user data filtered by user name (accessible by users with role "users" and "admin").
- `GET /policies/user/{user_name}`: Get the list of policies linked to a user name (accessible by users with role "admin").
- `GET /users/policy/{policy_id}`: Get the user linked to a policy number (accessible by users with role "admin").

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd insurance_api
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

4. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```

5. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Testing

To run the tests, use the following command:
```sh
pytest
```

## License
This project is licensed under the MIT License.

shell
Copiar código

### requirements.txt

fastapi
uvicorn
httpx
pydantic
pytest


This should give you a good starting point to implement the Web API following the hexagonal architecture pattern in Python using FastAPI. Make sure to adapt and extend this code as needed to fit all your requirements.