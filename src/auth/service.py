from __future__ import annotations

from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends
from uuid import UUID, uuid4
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from src.entities.user import User
from . import model
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..exceptions import AuthenticationError, UserAlreadyExistsError
import logging
import os

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        logging.warning(f"Invalid email or password for user {email}")
        return False
    return user

def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def verify_token(token: str) -> model.TokenData:
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM") ])
        user_id: str = payload.get("id")
        return model.TokenData(user_id=user_id)
    except PyJWTError:
        logging.warning(f"Could not validate credentials for token {token}")
        raise AuthenticationError("Could not validate credentials")

def register_user(db: Session, register_user_request: model.RegisterUserRequest) -> User:
    try:
        if db.query(User).filter(User.email == register_user_request.email).first():
            logging.warning(f"User with email {register_user_request.email} already exists")
            raise UserAlreadyExistsError(f"{register_user_request.email}")
        user = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password=get_password_hash(register_user_request.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        raise e

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> model.TokenData:
    return verify_token(token)

CurrentUser = Annotated[model.TokenData, Depends(get_current_user)]

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session) -> model.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError("Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, user.id, access_token_expires)
    return model.Token(access_token=access_token, token_type="bearer")
