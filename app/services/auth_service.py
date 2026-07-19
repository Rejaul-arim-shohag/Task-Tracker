from typing import Dict, Optional

from app.schemas.auth import LoginRequest, SignupRequest
from app.utils.security import create_access_token, hash_password, verify_password

_users_db: Dict[str, Dict[str, str]] = {}


def reset_users() -> None:
    _users_db.clear()


def signup_user(payload: SignupRequest) -> Dict[str, str]:
    username = payload.username.lower()
    if username in _users_db:
        raise ValueError("Username already exists")

    _users_db[username] = {
        "username": payload.username,
        "email": payload.email,
        "password": hash_password(payload.password),
    }
    return {"message": "User registered successfully"}


def login_user(payload: LoginRequest) -> Dict[str, str]:
    username = payload.username.lower()
    user = _users_db.get(username)
    if not user or not verify_password(payload.password, user["password"]):
        raise ValueError("Invalid username or password")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
