from fastapi import APIRouter
from app.data.airlines import AIRLINES

router = APIRouter(
    prefix="/airlines",
    tags=["Airlines"]
)


# =====================================================
# GET ALL AIRLINES
# =====================================================

@router.get("/")
def get_airlines():

    return {

        "total": len(AIRLINES),
        "airlines": AIRLINES

    }


# =====================================================
# GET SINGLE AIRLINE
# =====================================================

@router.get("/{code}")
def get_airline(code: str):

    code = code.upper()

    airline = next(
        (a for a in AIRLINES if a["code"] == code),
        None
    )

    if not airline:

        return {"error": "Airline not found"}

    return airline