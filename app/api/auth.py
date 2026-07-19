from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserInfoResponse
from app.services.auth_service import get_user_info_from_token, login_user, signup_user

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer(auto_error=True)


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


@router.get("/me", response_model=UserInfoResponse)
def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        return get_user_info_from_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
