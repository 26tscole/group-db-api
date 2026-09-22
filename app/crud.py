from typing import Generic, Iterable, Mapping, Sequence, Type, TypeVar
from unittest import result
from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

CONDITION_BUILDERS = {
    "eq": lambda column, value: column == value,
    "gt": lambda column, value: column > value,
    "gte": lambda column, value: column >= value,
    "lt": lambda column, value: column < value,
    "lte": lambda column, value: column <= value,
    "contains": lambda column, value: column.ilike(f"%{value}%"),
    "startswith": lambda column, value: column.ilike(f"{value}%"),
}


def build_filters(
    model: Type[ModelType],
    params: Mapping[str, str],
    allowed_fields: Iterable[str] | None = None,
) -> dict:
    """Turn raw query-string params into typed filters, ignoring keys that
    aren't columns on `model` (e.g. FastAPI/pagination params).

    Pass `allowed_fields` to further restrict which columns callers may filter
    on (e.g. only ID columns, not dates)."""
    columns = {c.name: c.type.python_type for c in model.__table__.columns}
    if allowed_fields is not None:
        columns = {
            name: py_type for name, py_type in columns.items() if name in allowed_fields
        }
    filters = {}
    for key, value in params.items():
        if key not in columns or value in (None, ""):
            continue
        try:
            filters[key] = columns[key](value)
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail=f"Invalid value for '{key}'")
    return filters


def build_conditions(
    model: Type[ModelType],
    params: Mapping[str, str],
    allowed_fields: Iterable[str] | None = None,
) -> list[ColumnElement[bool]]:
    columns = {column.name: column for column in model.__table__.columns}

    if allowed_fields is not None:
        columns = {
            name: column for name, column in columns.items() if name in allowed_fields
        }

    conditions = []

    for raw_key, raw_value in params.items():
        if raw_value in (None, ""):
            continue

        if "__" in raw_key:
            field_name, operator = raw_key.split("__", 1)
        else:
            field_name, operator = raw_key, "eq"

        if field_name not in columns:
            continue

        column = columns[field_name]

        try:
            value = TypeAdapter(column.type.python_type).validate_python(raw_value)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value for '{field_name}'",
            )

        if operator not in CONDITION_BUILDERS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported filter operator '{operator}'",
            )

        conditions.append(CONDITION_BUILDERS[operator](column, value))

    return conditions


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Reusable get/create/update/delete helper bound to one SQLAlchemy model.

    Filter kwargs (e.g. get_by(db, debt_id=1)) must match model column names.
    """

    def __init__(self, model: Type[ModelType], not_found_detail: str | None = None):
        self.model = model
        self.not_found_detail = not_found_detail or f"{model.__name__} not found"

    def get_by(self, db: Session, **filters) -> ModelType:
        result = db.scalar(select(self.model).filter_by(**filters))
        if not result:
            raise HTTPException(status_code=404, detail=self.not_found_detail)
        return result

    def get_many_by(self, db: Session, **filters) -> Sequence[ModelType]:
        result = db.scalars(select(self.model).filter_by(**filters)).all()
        if not result:
            raise HTTPException(status_code=404, detail=self.not_found_detail)
        return result

    def get_all(self, db: Session) -> Sequence[ModelType]:
        result = db.scalars(select(self.model)).all()
        if not result:
            raise HTTPException(
                status_code=404, detail=f"No {self.model.__name__} records found"
            )
        return result

    def search(self, db: Session, filters: dict) -> Sequence[ModelType]:
        """get_all when no filters are supplied, otherwise get_many_by(**filters)."""
        return self.get_all(db) if not filters else self.get_many_by(db, **filters)

    def search_conditions(
        self,
        db: Session,
        conditions: list[ColumnElement[bool]],
    ) -> Sequence[ModelType]:
        statement = select(self.model).where(*conditions)
        result = db.scalars(statement).all()

        if not result:
            raise HTTPException(
                status_code=404,
                detail=self.not_found_detail,
            )
        return result

    def require_filters(self, filters: dict) -> dict:
        if not filters:
            raise HTTPException(
                status_code=400,
                detail="At least one filter query parameter is required",
            )
        return filters

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> ModelType:
        db.delete(db_obj)
        db.commit()
        return db_obj

    def delete_many(
        self, db: Session, db_objs: Sequence[ModelType]
    ) -> Sequence[ModelType]:
        for db_obj in db_objs:
            db.delete(db_obj)
        db.commit()
        return db_objs

    def delete_all(self, db: Session) -> Sequence[ModelType]:
        db_objs = self.get_all(db)
        for db_obj in db_objs:
            db.delete(db_obj)
        db.commit()
        return db_objs
