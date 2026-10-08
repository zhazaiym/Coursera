# from mysite.database.models import Application, User, RoleChoices, Course, CourseStatusChoices, UserStatusChoices
# from mysite.database.schema import ApplicationInputSchema, ApplicationOutSchema
# from mysite.database.db import SessionLocal
# from mysite.api.auth import get_current_user
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, HTTPException, Depends
# from typing import List
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import (
    Application,
    User,
    RoleChoices,
    UserStatusChoices,
    Course,
    CourseStatusChoices,
    ApplicationStatusChoices,
)
from mysite.database.schema import (
    ApplicationInputSchema,
    ApplicationOutSchema, ApplicationUpdateSchema,
)
from mysite.api.auth import get_current_user

application_router = APIRouter(prefix='/application', tags=['Application'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@application_router.post(
    "/",
    response_model=ApplicationOutSchema
)
async def create_application(
    application: ApplicationInputSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Заявка түзө ала турган адам студент болушу керек
    if current_user.role != RoleChoices.student:
        raise HTTPException(
            status_code=403,
            detail="Создать заявку может только студент"
        )

    # Курсту табабыз
    course_db = (
        db.query(Course)
        .filter(Course.id == application.course_id)
        .first()
    )

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай курс жок"
        )

    # FREE студентке FREE курс гана жеткиликтүү
    if (
        current_user.user_status == UserStatusChoices.free
        and course_db.status != CourseStatusChoices.free
    ):
        raise HTTPException(
            status_code=403,
            detail="Free студент может создать заявку только на бесплатный курс"
        )

    # Pydantic объектти dict кылабыз
    application_data = application.model_dump()

    # Авторизациядан келген user'дин id'син алабыз
    application_data["student_id"] = current_user.id

    # Азырынча менеджер дайындала элек
    application_data["manager_id"] = None

    # Жаңы заявканын статусу
    application_data["status"] = ApplicationStatusChoices.new

    # Application түзөбүз
    application_db = Application(**application_data)

    db.add(application_db)
    db.commit()
    db.refresh(application_db)

    return application_db


@application_router.get('/', response_model=List[ApplicationOutSchema])
async def list_application(db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Список заявок может смотреть только менеджер')
    return db.query(Application).all()


@application_router.get('/{application_id}/', response_model=ApplicationOutSchema)
async def detail_application(application_id: int, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Заявку может смотреть только менеджер')
    application = db.query(Application).filter(Application.id==application_id).first()
    if not application:
        raise HTTPException(detail='Мындай заявка жок', status_code=404)
    return application


@application_router.put("/{application_id}/", response_model=ApplicationOutSchema)
async def update_application(
    application_id: int,
    application: ApplicationUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Только manager может изменить application
    if current_user.role != RoleChoices.manager:
        raise HTTPException(
            status_code=403,
            detail="Заявканы только manager өзгөртө алат"
        )

    application_db = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай заявка жок"
        )

    # Manager өзү manager_id болуп жазылсын
    application_db.manager_id = current_user.id

    # Status өзгөртүү
    application_db.status = application.status

    db.commit()
    db.refresh(application_db)

    return application_db

@application_router.delete('/{application_id}/', response_model=dict)
async def delete_application(application_id: int, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Удалить заявку может только менеджер')
    application_db = db.query(Application).filter(Application.id==application_id).first()
    if not application_db:
        raise HTTPException(detail='Мындай заявка жок', status_code=404)
    db.delete(application_db)
    db.commit()
    return {'message': 'Заявка удалить болду'}
