from typing import Type
from django.db import models
from rest_framework import serializers


class ModelSerializerBase(serializers.ModelSerializer):
    """Default functionality for model serializer."""

    datetime_format = "%Y-%m-%d %H:%M:%S"

    id = serializers.IntegerField(label="ID", read_only=True)

    created_at = serializers.DateTimeField(format=datetime_format, read_only=True, required=False, allow_null=True)
    updated_at = serializers.DateTimeField(format=datetime_format, read_only=True, required=False, allow_null=True)

    class Meta:
        read_only_fields = ["id", "created_at", "updated_at"]

    @property
    def model_class(self) -> Type[models.Model]:
        return self.Meta.model

    @property
    def readable_field_names(self) -> list[str]:
        """Get list of all fields in serializer that can be read."""

        return [key for key in self.get_fields().keys()]

    @property
    def writable_field_names(self) -> list[str]:
        """Get list of all fields that can be written to."""

        return [key for key, value in self.get_fields().items() if value.read_only is False]

    @property
    def readonly_field_names(self) -> list[str]:
        """Get list of all fields that can only be read, not written."""

        return [key for key, value in self.get_fields().items() if value.read_only is True]

    @property
    def required_field_names(self) -> list[str]:
        """Get list of all fields that must be written to on object creation."""

        return [key for key, value in self.fields.items() if value.required is True and value.read_only is False]

    @property
    def unique_field_names(self) -> list[str]:
        """Get list of all fields that can be used to unique identify models."""

        model_fields = self.model_class._meta.get_fields()
        unique_fields = [
            field for field in model_fields if getattr(field, "primary_key", False) or getattr(field, "_unique", False)
        ]
        unique_field_names = [field.name for field in unique_fields]

        return [field for field in self.readable_field_names if field in unique_field_names]

    @property
    def related_field_names(self) -> list[str]:
        """List of fields that inherit RelatedField, representing foreign key relations."""

        return [key for key, value in self.get_fields().items() if isinstance(value, serializers.RelatedField)]

    @property
    def many_related_field_names(self) -> list[str]:
        """List of fields that inherit ManyRelatedField, representing M2M relations."""

        return [key for key, value in self.get_fields().items() if isinstance(value, serializers.ManyRelatedField)]

    @property
    def any_related_field_names(self) -> list[str]:
        """List of fields that are single or many related."""

        return self.related_field_names + self.many_related_field_names
