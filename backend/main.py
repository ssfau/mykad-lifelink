from fastapi import FastAPI 
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

@app.get("/health")
def root_health():
    return {"Hello":"Health check positive"}

@app.get("/")
def homepage_quickreturn():
    return {"Hello":"Homepage quick return"}