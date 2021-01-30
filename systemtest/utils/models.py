from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Validators:
    twelve_chars = RegexValidator(r"^[a-zA-Z0-9]{12}$")
    seven_chars = RegexValidator(r"^[a-zA-Z0-9]{7}$")
    four_chars = RegexValidator(r"^[a-zA-Z0-9]{4}$")
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
