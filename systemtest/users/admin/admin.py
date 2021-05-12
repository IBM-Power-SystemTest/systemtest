from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from systemtest.users import models
from systemtest.utils.models import AbstractOptionsModelAdmin


@admin.register(models.Department)
class DepartmentAdmin(AbstractOptionsModelAdmin):
    """
    Model admin for Department
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
    """

    pass


@admin.register(models.Job)
class JobAdmin(AbstractOptionsModelAdmin):
    """
    Model admin for Job
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
    """

    pass


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    """
    Model admin for User
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-options
    """

    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "department",
        "email",
        "is_active",
        "is_staff",
        "shift"
    )
    list_editable = (
        "first_name",
        "last_name",
        "email",
        "shift",
    )
    list_display_links = (
        "pk",
        "username",
        "department",
    )
    list_filter = (
        "groups__name",
        "is_active",
        "is_staff",
        "is_superuser",
        "shift",
        "department__name",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
