from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.db import Base, engine
from backend.auth import create_session
from backend.routers.doctor import router as doctor_router
from backend.routers.patient import router as patient_router
from backend.routers.clinicadmin import router as clinicadmin_router
import os

# Detect if running on Vercel (serverless) vs local development vs Railway
root_path = "/api" if os.getenv("VERCEL") else None
app = FastAPI(root_path=root_path)

# Serve static frontend files (only in production/Railway, not in local dev)
# In local dev, frontend is served separately on port 8080
if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PORT"):
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(project_root, "frontend")
    
    # Mount static files (CSS, JS, images, etc.)
    if os.path.exists(frontend_dir):
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")
        app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
        app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
        
        # Mount login pages
        login_dir = os.path.join(frontend_dir, "loginPages")
        if os.path.exists(login_dir):
            app.mount("/loginPages", StaticFiles(directory=login_dir), name="loginPages")
        
        # Mount pages
        pages_dir = os.path.join(frontend_dir, "pages")
        if os.path.exists(pages_dir):
            app.mount("/pages", StaticFiles(directory=pages_dir), name="pages")

# Configure CORS to allow frontend requests (including file:// protocol with null origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development (including null)
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers including Authorization
    expose_headers=["*"],  # Expose all headers to the frontend
)

Base.metadata.create_all(bind=engine)

# Include API routers
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
    """Serve index.html in production, or return JSON in API-only mode"""
    if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PORT"):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        index_path = os.path.join(project_root, "frontend", "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    return {"Hello":"Homepage quick return"}

# Serve HTML files directly (for production)
@app.get("/index.html")
def serve_index():
    """Serve index.html"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(project_root, "frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}

# Note: FastAPI serves routes in order, so API routes (above) are checked first
# Static file mounts handle CSS/JS/assets
# HTML files are served via explicit routes or the mounts above

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