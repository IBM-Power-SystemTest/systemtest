from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from systemtest.users import models, forms

User = get_user_model()


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


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    # fieldsets = (
    #     (
    #         "User", {"fields": ("name",)}
    #     ),
    # ) + (auth_admin.UserAdmin.fieldsets,)

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
    search_fields = ("name",)
