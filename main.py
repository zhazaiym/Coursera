from fastapi import FastAPI
from mysite.database.db import Base, engine
from mysite.api import auth, category, course, study_group, application, enrollment, chain
import uvicorn


Base.metadata.create_all(bind=engine)

coursera = FastAPI(title='Coursera')


coursera.include_router(auth.auth_router)
coursera.include_router(category.category_router)
coursera.include_router(course.course_router)
coursera.include_router(study_group.study_group_router)
coursera.include_router(application.application_router)
coursera.include_router(enrollment.enrollment_router)
coursera.include_router(chain.chain_router)


if __name__ == '__main__':
    uvicorn.run(coursera, host='127.0.0.1', port=8000)