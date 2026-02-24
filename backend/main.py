from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import arv

app = FastAPI(title="Revolt Underwriting Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(arv.router)

@app.get("/")
def read_root():
    return {"message": "Revolt Underwriting Engine is live"}
