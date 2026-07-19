from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.task import TaskCreateRequest, TaskDeleteResponse, TaskResponse, TaskUpdateRequest
from app.services.auth_service import get_user_info_from_token
from app.services.task_service import create_task, delete_task, get_all_tasks, get_task_by_id, update_task

router = APIRouter(prefix="/tasks", tags=["tasks"])
bearer_scheme = HTTPBearer(auto_error=True)


def _get_user_id_from_token(credentials: HTTPAuthorizationCredentials) -> int:
    user = get_user_info_from_token(credentials.credentials)
    return user["id"]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_api(
    payload: TaskCreateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        user_id = _get_user_id_from_token(credentials)
        return create_task(user_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=List[TaskResponse])
def get_all_tasks_api(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        user_id = _get_user_id_from_token(credentials)
        return get_all_tasks(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id_api(
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        user_id = _get_user_id_from_token(credentials)
        return get_task_by_id(user_id, task_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_api(
    task_id: int,
    payload: TaskUpdateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        user_id = _get_user_id_from_token(credentials)
        return update_task(user_id, task_id, payload)
    except ValueError as exc:
        error_text = str(exc)
        if error_text == "No fields provided to update":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_text) from exc
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_text) from exc


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
def delete_task_api(
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        user_id = _get_user_id_from_token(credentials)
        return delete_task(user_id, task_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
