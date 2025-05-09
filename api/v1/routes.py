from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class AuthResponse(BaseModel):
    message: str
    token: Optional[str] = None

@router.post("/register", response_model=AuthResponse)
async def register_user(user: RegisterRequest):
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    hashed_pwd = hash_password(user.password)
    add_user(user.username, user.email, hashed_pwd)

    return {"message": "User registered successfully. Please login."}

@router.post("/login", response_model=AuthResponse)
def login_user(user: LoginRequest):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"message": "Login successful", "token": access_token}

@router.get("/home")
def home_page():
    return {"message": "Welcome to AI Study Buddy APP"}
