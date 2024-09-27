from fastapi import APIRouter, Depends, HTTPException

from database import get_repository
from models import User
from repository import UserRepository
from schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Работа с пользователем"],
)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, repository: UserRepository = Depends(get_repository)):
    db_user = User(full_name=user.full_name)
    return repository.create_user(db_user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, repository: UserRepository = Depends(get_repository)):
    db_user = repository.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, repository: UserRepository = Depends(get_repository)):
    db_user = repository.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.full_name = user.full_name
    return repository.update_user(db_user)

@router.delete("/{user_id}")
def delete_user(user_id: int, repository: UserRepository = Depends(get_repository)):
    db_user = repository.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    repository.delete_user(user_id)
    return {"detail": "User deleted"}
