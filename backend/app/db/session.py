import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------
# ABSOLUTE BASE DIRECTORY (VERY IMPORTANT)
# -------------------------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# -------------------------------------------------
# SQLITE DATABASE (ONE SINGLE FILE ONLY)
# -------------------------------------------------
DATABASE_PATH = os.path.join(BASE_DIR, "travel.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# -------------------------------------------------
# ENGINE
# -------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -------------------------------------------------
# SESSION
# -------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------
# DEPENDENCY
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()