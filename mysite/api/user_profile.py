from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import User
from mysite.database.schema import UserInputSchema, UserOutSchema
from mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

user_router = APIRouter(prefix='/users', tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get('/', response_model=List[UserOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get('/{user_id}/', response_model=UserOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return user_db


@user_router.put('/{user_id}/', response_model=dict)
async def update_user(user_id: int, user: UserInputSchema,
                      db: Session = Depends(get_db)):

    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)


    for user_key, user_value in user.model_dump().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)

    return {'message': 'Пользователь озгорулду'}


@user_router.delete('/{user_id}/', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):

    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)


    db.delete(user_db)
    db.commit()

    return {'message': 'Пользователь удалить болду'}