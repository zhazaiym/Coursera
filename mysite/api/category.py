from fastapi import APIRouter, Depends, HTTPException

from mysite.api.auth import get_current_user
from mysite.database.models import Category, User
from mysite.database.schema import CategoryInputSchema, CategoryOutSchema
from mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session


category_router = APIRouter(prefix='/categories', tags=['Categories'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='создать категорию может только админ')
    return current_user


@category_router.post('/', response_model=CategoryOutSchema)
async def create_category(
    category: CategoryInputSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    category_db = Category(
        category_name=category.category_name
    )

    db.add(category_db)
    db.commit()
    db.refresh(category_db)

    return category_db

@category_router.get('/{category_id}/', response_model=CategoryOutSchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()

    if not category_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)

    return category_db


@category_router.put('/{category_id}/', response_model=dict)
async def update_category(
    category_id: int,
    category: CategoryInputSchema,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(Category.id == category_id).first()

    if not category_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)

    category_db.category_name = category.category_name

    db.commit()
    db.refresh(category_db)

    return {'massage': 'Категория успешно изменена!'}


@category_router.delete('/{category_id}/', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()

    if not category_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)

    db.delete(category_db)
    db.commit()

    return {'massage': 'Категория успешно удалена!'}