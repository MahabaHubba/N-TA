from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware



# Import routers
from app.routers import users, notifications

# The FastAPI class is used to create an instance of the FastAPI application, which serves as the main entry point for defining routes and handling requests.
app = FastAPI(title="N-TA Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "ws://localhost:5173",
        "http://localhost:3000",
        "https://n-ta.vercel.app"  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Creates the tables automatically based on the models defined in the models.py file.
# Runs when it starts up

models.Base.metadata.create_all(bind=engine)

# @app.get("/")
# def health_check():
#     return {"status": "ok"}

app.include_router(users.router, prefix="/api")
app.include_router(notifications.router)