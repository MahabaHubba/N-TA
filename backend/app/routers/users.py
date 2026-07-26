from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import asyncio

# Backgroundtasks allows you to runt tasks in the backgroun after returning a response.
# This is useful for tasks that mihgt take a long time to complete such as sending notifications to all connected clients after a new user registers.
from fastapi import BackgroundTasks


from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut
from app.deps import get_current_user, get_db
from app.core.security import create_access_token
from app.routers.notifications import manager

# APIRouter allows you to create modular route handlers that can be easily included in the main application.
router = APIRouter(prefix="", tags=["users"])
# The reason we use UserOut as the response model for the register endpoint is to ensure that we only return the relevant user information (id and email) without exposing sensitive data such as the hashed password. By using a response model, we can control the structure of the response and ensure that only the necessary information is included.
@router.post("/register", response_model=UserOut)
# background_tasks is used to run tasks in the background after returning a response. In this case, it is used to notify all connected clients about a new user registration.
def register(user: UserCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = crud_user.create_user(db, email=user.email, password=user.password)
    # Notify all connected clients about the new user registration
    background_tasks.add_task(manager.broadcast, f"New user registered: {new_user.email}")
    return new_user


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(current_user: UserOut = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}