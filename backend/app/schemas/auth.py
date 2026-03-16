from pydantic import BaseModel, EmailStr


# =========================
# REGISTER SCHEMA
# =========================
class Register(BaseModel):
    username: str
    email: EmailStr
    password: str


# =========================
# LOGIN SCHEMA
# =========================
class Login(BaseModel):
    username: str
    password: str