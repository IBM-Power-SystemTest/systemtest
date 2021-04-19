from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Validators:
    twelve_chars = RegexValidator(
        r"^[a-zA-Z0-9]{12}$",
        message="Only 12 chars alpha-numeric"
    )
    seven_chars = RegexValidator(
        r"^[a-zA-Z0-9]{7}$",
        message="Only 7 chars alpha-numeric"
    )
    four_chars = RegexValidator(
        r"^[a-zA-Z0-9]{4}$",
        message="Only 4 chars alpha-numeric"
    )
    eight_digits_max = MaxValueValidator(int("9" * 8))
    eight_digits_min = MinValueValidator(int("1"+"0"*7))


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
        "Name",
        help_text="List element",
        max_length=50,
        unique=True,
        uppercase=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
