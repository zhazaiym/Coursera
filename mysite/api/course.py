from fastapi import APIRouter, Depends, HTTPException

from mysite.api.auth import get_current_user
from mysite.database.models import Course, User
from mysite.database.schema import CourseInputSchema, CourseOutSchema
from mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session


course_router = APIRouter(prefix='/courses', tags=['Courses'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != 'teacher':
        raise HTTPException(status_code=403, detail='доступ запрещен')
    return current_user

@course_router.post('/', response_model=CourseOutSchema)
async def create_course(course: CourseInputSchema, db: Session = Depends(get_db)):
    course_db = Course(
        title=course.title,
        category=course.category,
        description=course.description,
        level=course.level,
        price=course.price,
        duration_weeks=course.duration_weeks,
        is_active=course.is_active,
        status=course.status
    )

    db.add(course_db)
    db.commit()
    db.refresh(course_db)

    return course_db


@course_router.get('/', response_model=List[CourseOutSchema])
async def list_course(db: Session = Depends(get_db)):
    return db.query(Course).all()


@course_router.get('/{course_id}/', response_model=CourseOutSchema)
async def detail_course(course_id: int, db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.id == course_id).first()

    if not course_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)

    return course_db


@course_router.put('/{course_id}/', response_model=dict)
async def update_course(
    course_id: int,
    course: CourseInputSchema,
    db: Session = Depends(get_db)
):
    course_db = db.query(Course).filter(Course.id == course_id).first()

    if not course_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)

    course_db.title = course.title
    course_db.category = course.category
    course_db.description = course.description
    course_db.level = course.level
    course_db.price = course.price
    course_db.duration_weeks = course.duration_weeks
    course_db.is_active = course.is_active
    course_db.status = course.status

    db.commit()
    db.refresh(course_db)

    return {'massage': 'Курс успешно изменен!'}


@course_router.delete('/{course_id}/', response_model=dict)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.id == course_id).first()

    if not course_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)

    db.delete(course_db)
    db.commit()

    return {'massage': 'Курс успешно удален!'}