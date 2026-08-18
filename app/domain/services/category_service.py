from time import perf_counter

from app.config import get_settings
from app.datasource.cache.redis import RedisCacheBackend
from app.datasource.repositories.category_repository import CategoryRepository
from app.web.schemas.category import CategoryCreateSchema, CategorySchema
from sqlalchemy.orm import Session


class CategoryNotFound(Exception):
    """Category not found"""


settings = get_settings()


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)
        self.cache = RedisCacheBackend(settings.REDIS_URL, settings.cache_ttl_seconds)

    def list_categories(self) -> list[CategorySchema]:
        start = perf_counter()
        cached_categories = self.cache.get(settings.cache_categories_key)
        if cached_categories is not None:
            print(perf_counter() - start)
            return cached_categories

        categories_orm = self.category_repository.get_all()
        categories_read = [
            CategorySchema.model_validate(category) for category in categories_orm
        ]

        categories_for_cache = [
            CategorySchema.model_validate(category) for category in categories_read
        ]
        self.cache.set(settings.cache_categories_key, categories_for_cache)
        print(perf_counter() - start)
        return categories_read

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        self.cache.delete(settings.cache_categories_key)
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(
        self, category_id: str, category_update: CategoryCreateSchema
    ) -> CategorySchema:
        self.cache.delete(settings.cache_categories_key)
        category_for_update = self.category_repository.get_by_id(
            category_id=category_id
        )
        if not category_for_update:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        if category_update.name is not None:
            category_for_update.name = category_update.name
        self.db.commit()
        return CategorySchema.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        self.cache.delete(settings.cache_categories_key)
        category_for_delete = self.category_repository.get_by_id(
            category_id=category_id
        )
        if not category_for_delete:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        self.category_repository.delete(category_for_delete)
        self.db.commit()
