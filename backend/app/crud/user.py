from math import e
from sqlalchemy.orm import Session
from app.db import models
from app.core.security import hash_password, verify_password

# get use by email
def get_user_by_email(db: Session, email: str):
    # query the database for a user with the specified email and return the first result
    return db.query(models.User).filter(models.User.email == email).first()

# create user
def create_user(db: Session, email: str, password: str):
    # hash the password using the hash_password function and create a new user object with the email and hashed password
    hashed_password = hash_password(password)
    db_user = models.User(email=email, hashed_password=hashed_password)
    # add the new user tot he database, commit the transaction, refresh the user object to get the updated data from the database, and return the user object
    db.add(db_user)
    # commit the transaction to save the new user to the database, refresh the user object to get the updated data from the database, and return the user object
    db.commit()
    # refresh the user object to get the updated data from the database, and return the user object
    db.refresh(db_user)
    return db_user

# authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user