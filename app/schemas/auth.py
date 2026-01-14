from pydantic import BaseModel, EmailStr
from typing import List
from app.schemas.base import ApiResponse

# Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    app_code: str

class UserInfo(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    roles: List[str]

class LoginData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo

LoginResponse = ApiResponse[LoginData]

# Register
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    app_code: str

class RegisterData(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None

RegisterResponse = ApiResponse[RegisterData]
