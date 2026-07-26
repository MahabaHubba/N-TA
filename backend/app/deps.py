from app.db.database import SessionLocal
# Dependency that provides a database session to the path operations
from typing import Generator

from fastapi import Depends,HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
# The jose library is used for encoding and decoding JSON Web Tokens (JWTs), which are commonly used for authentication and authorization in web applications.
from jose import JWTError, jwt

from app.core.config import settings
from app.db import models

# Oauth2bearer is a class that handles oAUth2 authentication using bearer tokens.
# 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def get_db() -> Generator:
    # Create a new database session using the SessionLocal factory
    db = SessionLocal()
    try:
        # Yield the database session to the caller, allowing them to use it for database operations
        yield db
    finally:
        # Ensure that the database session is closed after use, preventing resource leaks
        db.close()

   
def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> models.User:
    # This function is a dependency that retrieves the current user based on the provided token.
    # It decodes the JWT token to extract the user's email and then queries the database to find the corresponding user.
    # If the token is invalid or the user is not found, it raises an HTTPException with a 401 status code.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
