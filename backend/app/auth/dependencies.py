from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.session import get_db
from app.core.config import settings
from app.models.user import User
from app.models.admin import Admin

# This creates the Bearer token dependency
security = HTTPBearer()


# =====================================================
# GET CURRENT USER OR ADMIN
# =====================================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    if not credentials:
        raise HTTPException(401, "Not authenticated")

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        print("TOKEN PAYLOAD:", payload)  # DEBUG

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(401, "Invalid token")

    # =====================================================
    # ADMIN LOGIN
    # =====================================================
    if payload.get("role") == "admin":

        admin_id = payload.get("admin_id")

        if not admin_id:
            raise HTTPException(401, "Invalid admin token")

        admin = db.query(Admin).filter(
            Admin.id == admin_id
        ).first()

        if not admin:
            raise HTTPException(401, "Admin not found")

        # attach role dynamically
        admin.role = "admin"

        print("AUTHENTICATED ADMIN:", admin.email)

        return admin


    # =====================================================
    # USER LOGIN
    # =====================================================
    user_id = payload.get("id")

    if not user_id:
        raise HTTPException(401, "Invalid user token")

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(401, "User not found")

    user.role = "user"

    print("AUTHENTICATED USER:", user.email)

    return user