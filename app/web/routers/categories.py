from app.domain.services.category_service import CategoryService
from app.web.dependencies import get_category_service
from app.web.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/categories")


@router.get("")
def read_categories(
    category_service: CategoryService = Depends(get_category_service),
) -> list[CategorySchema]:
    return category_service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service),
) -> CategorySchema:
    return category_service.create_category(category_create=payload)


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryService = Depends(get_category_service),
):
    try:
        return category_service.update_category(
            category_id=category_id, category_update=payload
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str, category_service: CategoryService = Depends(get_category_service)
) -> None:
    try:
        return category_service.delete_category(category_id=category_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
