from app.datasource.repositories.category_repository import CategoryRepository
from app.web.schemas.category import CategoryCreateSchema, CategorySchema
from sqlalchemy.orm import Session


class CategoryNotFound(Exception):
    """Category not found"""

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()  # noqa: F821
        return [CategorySchema.model_validate(category) for category in categories_orm]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(self, category_id: str,category_update: CategoryCreateSchema) -> CategorySchema:
        category_for_update = self.category_repository.get_by_id(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        if category_update.name is not None:
            category_for_update.name = category_update.name
        self.db.commit()
        return CategorySchema.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repository.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        self.category_repository.delete(category_for_delete)
        self.db.commit()