from pydantic import BaseModel, EmailStr


# ==========================================
# ADMIN REGISTER SCHEMA
# ==========================================

class AdminRegister(BaseModel):

    name: str

    email: EmailStr

    password: str


# ==========================================
# ADMIN LOGIN SCHEMA
# ==========================================

class AdminLogin(BaseModel):

    email: EmailStr

    password: str