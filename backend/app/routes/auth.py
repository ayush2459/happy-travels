from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin
from app.auth.utils import (
    get_password_hash,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# =====================================
# REGISTER
# =====================================

@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        (User.username == data.username) |
        (User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        is_admin=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "User registered successfully"
    }


# =====================================
# LOGIN
# =====================================

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form.username
    ).first()

    if not user or not verify_password(
        form.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "id": user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }