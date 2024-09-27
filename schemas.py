from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str

class UserUpdate(BaseModel):
    full_name: str

class UserResponse(BaseModel):
    id: int
    full_name: str
