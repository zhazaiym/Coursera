from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from typing import Optional

from mysite.database.db import SessionLocal
from mysite.database.models import User
from mysite.database.schema import (UserLoginSchema, CurrentUserSchema, UserOutSchema, UserInputSchema)
from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_LIFETIME)


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
auth_router = APIRouter(prefix='/auth', tags=['Auth'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get('sub'))
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,detail='Access token мөөнөтү бүттү')
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401,detail='Access token туура эмес')
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=401,detail='Мындай колдонуучу базада жок')
    return user_db


def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


@auth_router.post("/register/", response_model=dict)
async def register(user: UserInputSchema,db: Session = Depends(get_db)):
    email_db = db.query(User).filter(User.email == user.email).first()
    if email_db:
        raise HTTPException(status_code=400,detail='Мындай почта бар')
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role,
        user_status=user.user_status
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Сиз ийгиликтүү катталдыңыз"
    }


@auth_router.post('/login/',response_model=dict)
async def login(user:UserLoginSchema,db:Session=Depends(get_db)):
    user_db=(
        db.query(User)
        .filter(User.email==user.email)
        .first()
    )

    if not user_db or not verify_password(user.password,user_db.password):
        raise HTTPException(status_code=401,detail='Сиз жазган маалымат туура эмес')

    access_token=create_access_token({'sub':str(user_db.id)})

    return {
        'access_token':access_token,
        'token_type':'bearer',
    }


@auth_router.get('/verify/',response_model=CurrentUserSchema)
async def verify_access_token(current_user:User=Depends(get_current_user)):
    return current_user

@auth_router.get('/me/', response_model=UserOutSchema)
async def user_me(profile: User = Depends(get_current_user)):
    return profile


@auth_router.put('/me/update/',response_model=dict)
async def update_me(user: UserInputSchema,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    current_user.full_name = user.full_name
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    current_user.role = user.role
    current_user.user_status = user.user_status

    db.commit()
    db.refresh(current_user)

    return {
        'message': 'Маалымат ийгиликтүү өзгөртүлдү'
    }


@auth_router.delete('/me/delete/',response_model=dict)
async def delete_me(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {
        'message': 'Аккаунт ийгиликтүү өчүрүлдү'}


