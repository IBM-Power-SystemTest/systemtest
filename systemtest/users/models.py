from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from systemtest.utils import models as utils_models

from datetime import date


class Departament(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "users_departament"


class Job(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "users_job"


class User(AbstractUser):
    """Default user for systemtest."""
    department = models.ForeignKey(
        to=Departament, on_delete=models.PROTECT, null=True, blank=True
    )
    job = models.ForeignKey(to=Job, on_delete=models.PROTECT, null=True, blank=True)

    modified = models.DateTimeField(auto_now=True)
    last_password_modified = models.DateField(default=date.today)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        db_table = "users_user"
