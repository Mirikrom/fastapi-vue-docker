from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import auth
from app.database.config import engine, Base
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlar
app.include_router(auth.router)






