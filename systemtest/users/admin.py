from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from systemtest.users import models


@admin.register(models.Departament)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk",)
    list_editable = ("name",)
    search_fields = ("pk", "name")


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk",)
    list_editable = ("name",)
    search_fields = ("pk", "name")


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    # inlines = (UserInline, )
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "department",
        "job",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
        "last_password_modified"
    )
    list_editable = (
        "first_name",
        "last_name",
        "email",
    )
    list_display_links = (
        "pk",
        "username",
        "department",
        "date_joined",
        "last_password_modified",
    )
    list_filter = ("groups__name", "is_active", "is_staff")

    search_fields = (
        "user__username",
        "user__group",
        "user__first_name",
        "user__last_name",
        "user__email",
        "department__name",
    )
