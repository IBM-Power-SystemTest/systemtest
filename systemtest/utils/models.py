"""
Utilities for Django Models
"""

from typing import Tuple, Union
from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Validators:
    """
    Utility for create a dinamic validators for Django Models
        References:
            https://docs.djangoproject.com/en/3.1/ref/validators/
    """

    @staticmethod
    def chars(qty: int) -> RegexValidator:
        """
        Creates a regex validator only for alphanumeric characters of a specified length

        Args:
            qty:
                Len of chars.

        Returns:
            RegexValidator.

            examples:
                RegexValidator(
                    regex='^[a-zA-Z0-9]{7}$',
                    message='Only 7 chars alpha-numeric'
                )
        """
        return RegexValidator(
            "^[a-zA-Z0-9]{" + str(qty) + "}$",
            message=f"Only {qty} chars alpha-numeric"
        )

    @staticmethod
    def digits(max_value: int, min_value: Union[int, None] = None, digits: bool = True) -> Tuple[MaxValueValidator, MinValueValidator]:
        """
        Generates a list with minimum and maximum validators or a maximum
        of digits.

        The default minimum is 0 if digit is False, and if digit is true
        and minimum is None the minimum number of those digits is assigned
        Such as 8 digits = Min(10000000) & Max(99999999)

        Args:
            max_value:
                Number for MaxValueValidator.
            min_value:
                Optional; Number for MinValueValidator.
            digits:
                Optional; If the maximum is by value or by number of digits.

        Returns:
            Tuple with two elements, the first the maximum validator and
            the second the minimum value.
            Tuple[MaxValueValidator, MinValueValidator]

            examples:
                ( MaxValueValidator(99999999), MinValueValidator(10000000) )

                ( MaxValueValidator(10), MinValueValidator(1) )
        """

        if digits:
            if not min_value:
                # If min_value is None set a min with a min value with this digits
                min_value = int("1"+"0"*(max_value - 1))
            max_value = int("9" * max_value)

        # Min value is not setted previusly the default is 0
        min_value = min_value if min_value else 0

        max_validator = MaxValueValidator(max_value)
        min_validator = MinValueValidator(min_value)
        return max_validator, min_validator


class CharFieldUpper(models.CharField):
    """
    A normal charfield, but add the option to be able to transform its
    value into uppercase
        References:
            https://docs.djangoproject.com/en/3.1/ref/models/fields/

    Attributes:
        uppercase: bool | False
            Indicates if the value is to be converted to uppercase
    """

    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop("uppercase", False)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value: str) -> str:
        """
        Inherits from CharField, after processing the value it transforms
        it to uppercase if so indicated

        Args:
            value:
                Value to be saved in the instance and then in the database

        Returns:
            Value processed by the original function but transformed
            (or not) in uppercase
        """
        value = super().get_prep_value(value)
        if self.is_uppercase and value:
            return value.upper()

        return value


class AbstractOptionsModel(models.Model):
    """
    Abstract model for tables with only name and id like table options
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        id:
            Change ID defaults to small auto increment (Max 255 values)
        name:
            Option name
        Meta:
            Model/table options
    """
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


class AbstractOptionsModelAdmin(admin.ModelAdmin):
    """
    Abstract admin model, like AbstractOptionsModel always need the same
    option for those kind of models.
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

    Attributes:
        list_display:
            To control which fields are displayed on the change list page
            of the admin.
        list_editable:
            A list of field names on the model which will allow editing on
            the change list page.
        search_fields:
            Enable a search box on the admin change list page.
    """
    list_display = ("pk", "name")
    list_editable = ("name",)
    search_fields = ("pk", "name")
