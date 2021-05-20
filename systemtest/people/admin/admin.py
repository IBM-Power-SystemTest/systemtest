from django.contrib import admin

from systemtest.people import models
from systemtest.utils.models import AbstractOptionsModelAdmin


@admin.register(models.PeopleType)
class PeopleTypeAdmin(AbstractOptionsModelAdmin):
    """
    Model admin
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
    """

    pass

@admin.register(models.PeopleStatus)
class PeopleStatusAdmin(AbstractOptionsModelAdmin):
    """
    Model admin
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
    """

    pass


@admin.register(models.PeopleRequirement)
class PeopleRequirementAdmin(admin.ModelAdmin):
    """
    Model admin
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-options
    """

    list_display = (
        "pk",
        "by_user",
        "for_user",
        "type",
        "description",
        "status",
        "start",
        "days",
        "created",
    )
    list_editable = (
        "start",
        "days",
        "description",
        "status",
    )
    search_fields = (
        "pk",
        "by_user",
        "for_user",
        "description",
    )
    list_filter = (
        "type",
        "status",
        "start",
        "created",
    )


@admin.register(models.PeopleHistory)
class PeopleHistory(admin.ModelAdmin):
    """
    Model admin
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-options
    """

    list_display = (
        "requirement",
        "status",
        "start",
        "days",
        "created",
    )
    search_fields = (
        "requirement__by_user",
        "requirement__for_user",
        "requirement__description",
    )
    list_filter = (
        "requirement__type",
        "status",
        "created",
    )
