from django.contrib import admin
from systemtest.quality import models
from systemtest.utils.models import AbstractOptionsModelAdmin


@admin.register(models.QualityStatus)
class QualityStatusAdmin(AbstractOptionsModelAdmin):
    """
    Model admin for QualityStatus
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
    """

    pass


@admin.register(models.QualitySystem)
class QualitySystemAdmin(admin.ModelAdmin):
    """
    Model admin for QualitySystem
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-options
    """

    list_display = (
        "workunit",
        "system_number",
        "product_line",
        "operation_number",
        "operation_status",
        "quality_status",
        "comment",
        "modified",
        "user",
    )
    list_editable = ("quality_status",)
    search_fields = (
        "system_number",
        "workunit",
        "user__username",
    )
    list_filter = (
        "operation_number",
        "operation_status",
        "product_line",
        "quality_status",
        ("modified", admin.DateFieldListFilter),
    )


@admin.register(models.QualityHistory)
class QualityHistoryAdmin(admin.ModelAdmin):
    """
    Model admin for QualityHistory
        References:
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-objects
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator
            https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-options
    """

    list_display = (
        "system",
        "operation_number",
        "operation_status",
        "quality_status",
        "comment",
        "user",
    )
    search_fields = (
        "system__workunit",
        "system__system_number",
        "user__username",
    )
    list_filter = (
        "operation_number",
        "operation_status",
        "system__product_line",
        "quality_status",
        ("created", admin.DateFieldListFilter),
    )
