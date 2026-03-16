from app.db.base_class import Base
from app.db.session import engine

# IMPORT ALL MODELS HERE (CRITICAL)
from app.models.user import User
from app.models.admin import Admin
from app.models.booking import Booking
from app.models.seat_lock import SeatLock

def init_db():
    Base.metadata.create_all(bind=engine)