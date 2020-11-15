from django.contrib import admin

from . import models


@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "url"]
    readonly_fields = ["code", "name", "small_logo_url", "medium_logo_url", "url"]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["account_user", "guid", "is_disabled"]
    readonly_fields = ["account_user", "guid", "is_disabled"]


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "institution",
        "user",
        "guid",
        "connection_status",
        "successfully_aggregated_at",
    ]
    readonly_fields = [
        "institution",
        "user",
        "aggregated_at",
        "connection_status",
        "guid",
        "name",
        "successfully_aggregated_at",
    ]
