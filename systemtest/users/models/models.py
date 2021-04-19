from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from systemtest.utils import models as utils_models


class Department(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "users_department"


class Job(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "users_job"


class User(AbstractUser):
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

    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users_user"
