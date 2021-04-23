from django.contrib import admin
from systemtest.quality import models
from systemtest.utils.models import AbstractOptionsModelAdmin


@admin.register(models.QualityStatus)
class QualityStatusAdmin(AbstractOptionsModelAdmin):
    pass


@admin.register(models.QualitySystem)
class QualitySystemAdmin(admin.ModelAdmin):
    list_display = (
        "workunit",
        "system_number",
        "product_line",
        "machine_type",
        "system_model",
        "quality_status",
        "created",
        "user",
    )
    list_editable = ("quality_status",)
    list_display_links = ("workunit",)
    search_fields = (
        "workunit",
        "system_number",
        "product_line",
    )
    search_fields = (
        "workunit",
        "system_number",
        "product_line",
    )


@admin.register(models.QualityHistory)
class QualityHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "system",
        "quality_status",
        "created",
        "user",
    )
    search_fields = (
        "workunit",
        "system_number",
        "product_line",
        "quality_status"
    )
