from django.contrib import admin

from .models import PhasmaDevice


@admin.register(PhasmaDevice)
class PhasmaDeviceAdmin(admin.ModelAdmin):
    list_display = ("mac", "name", "date_added")
    fieldsets = (
        ("Info", {"fields": ("mac", "name")}),
        ("Date added/updated", {"fields": ("date_added", "date_updated")})
    )
    readonly_fields = ("date_added", "date_updated")
    ordering = ("-date_added",)
