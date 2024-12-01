from typing import Any, ClassVar, Generic, MutableMapping, Optional, Self
from django.db import models

from utils.types import T


class ManagerBase(models.Manager, Generic[T]):
    """Extends django manager for improved db access."""

    def create(self, **kwargs) -> T:
        """Create new model."""
        return super().create(**kwargs)

    def find_one(self, **kwargs) -> Optional[T]:
        """Return first model matching query, or none."""
        return self.filter_one(**kwargs)

    def find_by_id(self, id: int) -> Optional[T]:
        """Return model if exists."""
        return self.find_one(id=id)

    def find(self, **kwargs) -> Optional[T]:
        """Return models matching kwargs, if exist."""
        return self.filter(**kwargs)

    def filter_one(self, **kwargs) -> Optional[T]:
        """Find object matching any of the fields (or)."""
        query = self.all().order_by("-id")

        for key, value in kwargs.items():
            res = query.filter(**{key: value})

            if res.exists():
                query = res

        if query.count() < self.count():
            return query.first()
        else:
            return None

    def get(self, *args, **kwargs) -> T:
        """Return object matching query, throw error if not found."""
        return super().get(*args, **kwargs)

    def get_by_id(self, id: int) -> T:
        """Return object with id, throw error if not found."""
        return self.get(id=id)

    def get_or_create(self, defaults: MutableMapping[str, Any] | None = None, **kwargs) -> tuple[T, bool]:
        return super().get_or_create(defaults, **kwargs)

    def update_one(self, id: int, **kwargs) -> Optional[T]:
        """Update model if it exists."""
        obj = self.find_by_id(id=id)

        if obj:
            self.filter(id=id).update(**kwargs)
            obj.refresh_from_db(using=self._db)

        return obj

    def update_many(self, query: dict, **kwargs) -> models.QuerySet[T]:
        """Update models with kwargs if they match query."""
        self.filter(**query).update(**kwargs)
        return self.filter(**query)

    def delete_one(self, id: int) -> Optional[T]:
        """Delete model if exists."""
        obj = self.find_by_id(id)

        if obj:
            self.filter(id=id).delete()

        return obj

    def delete_many(self, **kwargs) -> models.QuerySet[T]:
        """Delete models that match query."""
        objs = self.filter(**kwargs)
        objs.delete()

        return objs


class ModelBase(models.Model):
    """Default fields for all models."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    objects: ClassVar[ManagerBase[Self]] = ManagerBase[Self]()

    @classmethod
    def get_fields_list(cls, include_parents=True, exclude_read_only=False) -> list[str]:
        """Return a list of editable fields."""

        fields = [
            str(field.name)
            for field in cls._meta.get_fields(include_parents=include_parents)
            if (not exclude_read_only or (exclude_read_only and field.editable is True))
        ]

        return fields

    def __str__(self) -> str:
        if hasattr(self, "name"):
            return self.name
        elif hasattr(self, "display_name"):
            return self.display_name

        return super().__str__()

    class Meta:
        abstract = True
