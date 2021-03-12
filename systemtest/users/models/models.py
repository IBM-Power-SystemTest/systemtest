from datetime import date

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from systemtest.utils import models as utils_models


class department(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "users_department"


class Job(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "users_job"


class User(AbstractUser):
    department = models.ForeignKey(
        to=department, on_delete=models.PROTECT, null=True, blank=True
    )
    job = models.ForeignKey(to=Job, on_delete=models.PROTECT, null=True, blank=True)

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
