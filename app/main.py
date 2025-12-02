from fastapi import FastAPI

from app.database import Base, engine
from app.routers import (
    auth_router, 
    patients_router, 
    professionals_router, 
    units_router, 
    consultations_router,
    medical_records_router
    )

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vida Plus - SGHSS (Back-end)",
    version="0.1.0",
)


@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok"}


# Rotas
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(professionals_router)
app.include_router(units_router)
app.include_router(consultations_router)
app.include_router(medical_records_router)