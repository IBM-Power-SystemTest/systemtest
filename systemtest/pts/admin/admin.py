from django.contrib import admin
from systemtest.pts import models


@admin.register(models.RequestGroupWorkspace)
class RequestGroupWorkspaceAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk",)
    list_editable = ("name",)
    search_fields = ("pk", "name")


@admin.register(models.RequestStatus)
class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk",)
    list_editable = ("name",)
    search_fields = ("pk", "name")


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
        "part_number",
        "request_group_workspace",
        "is_loaner",
    )
    search_fields = (
        "pk",
        "system_number",
        "system_cell",
        "part_number",
        "part_description",
        "request_bay",
    )
    # filter_vertical = (
    #     'request_group_workspace',
    #     'is_loaner',
    # )


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
    )
    list_editable = (
        "request_status",
        "part_number",
        "serial_number",
        "ncm_tag",
    )
    list_display_links = ("pk", "request_group")
    search_fields = (
        "pk",
        "request_group",
        "ncm_tag",
    )
    # filter_vertical = (
    #     'request_status',
    # )


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
    list_display_links = (
        "request",
        "created",
    )
    search_fields = (
        "request",
        "serial_number",
        "request_status",
        "created",
        "user",
    )
    # filter_vertical = (
    #     'request_track_status',
    #     'created',
    #     'user'
    # )
