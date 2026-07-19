from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from app.services.auth_service import login_user, signup_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest):
    try:
        return signup_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    try:
        return login_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
