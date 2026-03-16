from pydantic import BaseModel, EmailStr


# =====================================
# REGISTER SCHEMA
# =====================================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


# =====================================
# LOGIN SCHEMA (Optional if using OAuth2 form)
# =====================================

class UserLogin(BaseModel):
    username: str
    password: str


# =====================================
# RESPONSE SCHEMA
# =====================================

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True