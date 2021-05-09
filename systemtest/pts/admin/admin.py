from django.contrib import admin

from systemtest.pts import models
from systemtest.utils.models import AbstractOptionsModelAdmin


@admin.register(models.RequestGroupWorkspace)
class RequestGroupWorkspaceAdmin(AbstractOptionsModelAdmin):
    pass


@admin.register(models.RequestStatus)
class RequestStatusAdmin(AbstractOptionsModelAdmin):
    pass


@admin.register(models.RequestGroup)
class RequestGroupAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "system_number",
        "system_cell",
        "part_number",
        "part_description",
        "request_group_workspace",
        "is_loaner",
        "is_vpd",
        "is_serialized",
        "qty",
    )
    list_editable = (
        "system_number",
        "system_cell",
        "part_description",
    )
    search_fields = (
        "pk",
        "system_number",
        "system_cell",
        "part_number",
        "part_description",
    )
    list_filter = (
        "request_group_workspace",
        "is_loaner",
        "is_vpd",
        "is_serialized",
    )


@admin.register(models.Request)
class ResquestAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "request_group",
        "request_status",
        "part_number",
        "serial_number",
        "modified",
        "ncm_tag",
        "user"
    )
    list_editable = (
        "request_status",
        "part_number",
        "serial_number",
    )
    search_fields = (
        "pk",
        "part_number",
        "serial_number",
        "ncm_tag",
        "user__username",
        "comment"
    )
    list_filter = (
        "request_status",
        ("modified", admin.DateFieldListFilter),
        "request_group__request_group_workspace",
        "request_group__is_loaner",
        "request_group__is_vpd",
        "request_group__is_serialized",
    )


@admin.register(models.RequestHistory)
class RequestHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "part_number",
        "serial_number",
        "request_status",
        "created",
        "comment",
        "user",
    )
    search_fields = (
        "request__pk",
        "part_number",
        "serial_number",
        "user__username",
    )
    list_filter = (
        "request_status",
        ("created", admin.DateFieldListFilter),
    )
