from django.contrib import admin
from systemtest.pts import models


@admin.register(models.RequestGroupWorkspace)
class RequestGroupWorkspaceAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk",)
    list_editable = ("name",)
    search_fields = ("pk", "name")


@admin.register(models.RequestGroupStatus)
class RequestGroupStatusAdmin(admin.ModelAdmin):
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


@admin.register(models.RequestNotNcmStatus)
class RequestNotNcmStatusAdmin(admin.ModelAdmin):
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
        "request_bay",
        "is_loaner",
        "is_vpd",
        "is_serialized",
        "qty",
        "request_group_status"
    )
    list_editable = (
        "system_number",
        "system_cell",
        "part_description",
        "part_number",
        "request_group_workspace",
        "request_bay",
        "is_loaner",
    )
    list_display_links = ("pk",)
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
        "ncm_tag",
        "not_ncm_status",
    )
    list_editable = (
        "request_status",
        "ncm_tag",
        "not_ncm_status"
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
        "serial_number",
        "request_track_status",
        "created",
        "user",
    )
    list_editable = (
        "serial_number",
        "request_track_status",
    )
    list_display_links = (
        "request",
        "created",
        "user"
    )
    search_fields = (
        "request",
        "serial_number",
        "request_track_status",
        "created",
        "user",
    )
    # filter_vertical = (
    #     'request_track_status',
    #     'created',
    #     'user'
    # )
