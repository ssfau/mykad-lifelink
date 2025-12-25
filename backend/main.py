from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db import Base, engine
from backend.auth import create_session
from backend.routers.doctor import router as doctor_router
from backend.routers.patient import router as patient_router
from backend.routers.clinicadmin import router as clinicadmin_router

app = FastAPI()  # root_path="/api" removed for local development (use only with reverse proxy)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers including Authorization
)

Base.metadata.create_all(bind=engine)

app.include_router(doctor_router, prefix="/doctor")
app.include_router(patient_router, prefix="/patient")
app.include_router(clinicadmin_router, prefix="/clinicadmin")

# Local development run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

""" WEBSITE HEALTH CHECK """

@app.get("/health")
def root_health():
    return {"Hello":"Health check positive"}

@app.get("/")
def homepage_quickreturn():
    return {"Hello":"Homepage quick return"}

""" MOCK AUTHENTICATION """

class MockLoginRequest(BaseModel):
    user_id: int
    role: str

@app.post("/auth/login")
def mock_login(data: MockLoginRequest):
    if data.role not in ["patient", "doctor", "clinic_admin"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid role")

    token = create_session(data.user_id, data.role)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": data.role
    }


"""
token requirement usage example:

@app.get("/scan")
def doctor_scan(session=Depends(require_role("doctor"))):
    return {"ok": True}
"""