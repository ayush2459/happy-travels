from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.routes.auth import router as auth_router
from app.routes.pricing import router as pricing_router
from app.routes.bookings import router as bookings_router
from app.routes.payment import router as payment_router
from app.routes.admin import router as admin_router
from app.routes.flights import router as flights_router
from app.routes.cities import router as cities_router
from app.db.init_db import init_db
init_db()
from app.db.session import engine
from app.db.base_class import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Happy Travels API",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROUTES
# =====================================================

app.include_router(auth_router)
app.include_router(bookings_router)
app.include_router(payment_router)
app.include_router(admin_router)
app.include_router(flights_router)
app.include_router(cities_router)
app.include_router(pricing_router)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {"status": "API running"}


# =====================================================
# FIX SWAGGER AUTH COMPLETELY
# =====================================================

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Happy Travels API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer"
        }
    }

    # DO NOT apply globally
    # Let Depends(security) handle it

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi