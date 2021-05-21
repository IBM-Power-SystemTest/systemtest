# Python
from datetime import date

# Django
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# APPs
from systemtest.utils import models as utils_models


class Department(utils_models.AbstractOptionsModel):
    """
    Departament table for users area
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "users_department"


class Job(utils_models.AbstractOptionsModel):
    """
    Job table for users role or position
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "users_job"


class User(AbstractUser):
    """
    Change the auth Django users
        References:
            https://docs.djangoproject.com/en/3.1/topics/auth/default/
            https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#substituting-a-custom-user-model

    Attributes:
        department:
            User's department or area
        job:
            User's role or position
        shift:
            User's shift
        mfs:
            User's MFS user if has it
        modified:
            DateTime form last update
        last_password_modified:
            Date from last change of password
    """

    department = models.ForeignKey(
        to=Department, on_delete=models.PROTECT, null=True, blank=True
    )
    job = models.ForeignKey(
        verbose_name="Job",
        to=Job,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    shift = models.PositiveSmallIntegerField(
        "Shift",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True, blank=True
    )
    mfs = utils_models.CharFieldUpper(
        "MFS",
        help_text="Manufactoring Floor System User",
        max_length=30,
        null=True,
        blank=True,
        uppercase=True,
    )
    modified = models.DateTimeField(auto_now=True)
    last_password_modified = models.DateField(default=date.today)

    def get_absolute_url(self) -> str:
        """
        Get url for user's detail view
            References:
                https://docs.djangoproject.com/en/3.1/ref/models/instances/#get-absolute-url
        Args:
            self:
                User instance

        Returns:
            URL for user detail

            example:
                '/users/alanv/
        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} [ {self.username} ]"

    class Meta:
        db_table = "users_user"
