from django.contrib import admin
from systemtest.quality import models
from systemtest.utils.models import AbstractOptionsModelAdmin


@admin.register(models.QualityStatus)
class QualityStatusAdmin(AbstractOptionsModelAdmin):
    pass

class QualityAbstractAdmin(admin.ModelAdmin):
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

@admin.register(models.QualitySystem)
class QualitySystemAdmin(QualityAbstractAdmin):
    pass

@admin.register(models.QualityHistory)
class QualityHistoryAdmin(QualityAbstractAdmin):
    list_editable = []
