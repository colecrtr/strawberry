from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["account_user", "guid", "is_disabled"]
    readonly_fields = ["account_user", "guid", "is_disabled"]
