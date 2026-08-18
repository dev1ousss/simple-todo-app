from app.config import get_settings
from app.datasource.cache.redis import RedisCacheBackend
from app.datasource.repositories.task_repository import TaskRepository
from app.web.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from sqlalchemy.orm import Session


class TaskNotFound(Exception):
    """Task not found"""


settings = get_settings()


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = RedisCacheBackend(settings.REDIS_URL, settings.cache_ttl_seconds)

    def list_tasks(self) -> list[TaskSchema]:
        cached_tasks = self.cache.get(settings.cache_tasks_key)
        if cached_tasks is not None:
            return cached_tasks

        tasks_orm = self.task_repository.get_all()

        task_read = [TaskSchema.model_validate(task) for task in tasks_orm]

        tasks_for_cache = [task.model_dump() for task in task_read]
        self.cache.set(settings.cache_tasks_key, tasks_for_cache)

        return task_read

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        self.cache.delete(settings.cache_tasks_key)
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        self.cache.delete(settings.cache_tasks_key)
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Task with id {task_id} not found")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        self.cache.delete(settings.cache_tasks_key)
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Task with id {task_id} not found")
        self.task_repository.delete(task_for_delete)
        self.db.commit()
