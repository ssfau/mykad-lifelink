import secrets
from datetime import datetime, timedelta
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException, Header
from backend.db import Base, engine
from backend.routers.doctor import router as doctor_router
from backend.routers.patient import router as patient_router

app = FastAPI(root_path="/api")

Base.metadata.create_all(bind=engine)

app.include_router(doctor_router, prefix="/doctor")
app.include_router(patient_router, prefix="/patient")

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
# meant for import

SESSIONS = {}
SESSION_TTL = timedelta(hours=1)

def create_session(user_id: int, role: str):
    token = secrets.token_urlsafe(32)

    SESSIONS[token] = {
        "user_id": user_id,
        "role": role,
        "issued_at": datetime.utcnow(),
        "expires": datetime.utcnow() + SESSION_TTL
    }

    return token

def get_session(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    session = SESSIONS.get(token)

    if not session:
        raise HTTPException(status_code=401)

    if session["expires"] < datetime.utcnow():
        raise HTTPException(status_code=401)

    return session

def require_auth(allowed_roles: list[str]):
    def checker(session=Depends(get_session)):
        if not session:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if session["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return session  # contains user_id, role
    return checker


class MockLoginRequest(BaseModel):
    user_id: int
    role: str

@app.post("/auth/login")
def mock_login(data: MockLoginRequest):
    if data.role not in ["patient", "doctor", "clinic_admin"]:
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