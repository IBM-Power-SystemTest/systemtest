from typing import Tuple, Union
from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Validators:
    @classmethod
    def chars(cls, qty: int) -> RegexValidator:
        return RegexValidator(f"^[a-zA-Z0-9]{qty}$")

    @classmethod
    def digits(
        cls, max_value: int, min_value: Union[int, None] = None, digits: bool = True
    ) -> Tuple[MaxValueValidator, MinValueValidator]:
        if digits:
            min_value = min_value if min_value else int("1"+"0"*(max_value - 1))
            max_value = int("9" * max_value)

        min_value = min_value if min_value else 0

        max_validator = MaxValueValidator(max_value)
        min_validator = MinValueValidator(min_value)
        return max_validator, min_validator


class CharFieldUpper(models.CharField):
    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop("uppercase", False)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value: str) -> str:
        value = super().get_prep_value(value)
        if self.is_uppercase and value:
            return value.upper()

        return value


class AbstractOptionsModel(models.Model):
    id = models.SmallAutoField(
        primary_key=True,
        unique=True,
        editable=False
    )
    name = CharFieldUpper(
        "Nombre",
        help_text="Elemento de la lista",
        max_length=50,
        unique=True,
        uppercase=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class AbstractOptionsModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk",)
    list_editable = ("name",)
    search_fields = ("pk", "name")
