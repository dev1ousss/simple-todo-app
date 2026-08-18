from app.datasource.database.session import get_db
from app.domain.services.category_service import CategoryService
from app.domain.services.task_service import TaskService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
