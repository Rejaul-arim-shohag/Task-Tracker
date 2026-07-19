from typing import Dict

from app.database.db import connection
from app.schemas.auth import LoginRequest, SignupRequest
from app.utils.security import create_access_token, hash_password, verify_password


def _ensure_users_table() -> None:
    if connection is None:
        return

    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
            """
        )
    connection.commit()


def signup_user(payload: SignupRequest) -> Dict[str, str]:
    _ensure_users_table()
    email = payload.email.lower()

    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = %s", (email,))
        if cursor.fetchone():
            raise ValueError("Email already exists")

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (payload.name, email, hash_password(payload.password)),
        )
    connection.commit()
    return {"message": "User registered successfully"}


def login_user(payload: LoginRequest) -> Dict[str, str]:
    _ensure_users_table()
    email = payload.email.lower()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name, email, password FROM users WHERE LOWER(email) = %s",
            (email,),
        )
        user = cursor.fetchone()

    if not user or not verify_password(payload.password, user["password"]):
        raise ValueError("Invalid email or password")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
