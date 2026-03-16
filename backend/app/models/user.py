from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):

    __tablename__ = "users"

    # =============================
    # PRIMARY KEY
    # =============================

    id = Column(Integer, primary_key=True, index=True)


    # =============================
    # USER INFO
    # =============================

    username = Column(String, unique=True, index=True, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)


    # =============================
    # ROLE
    # =============================

    is_admin = Column(Boolean, default=False)


    # =============================
    # RELATIONSHIP (FIXED)
    # =============================

    bookings = relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan"
    )