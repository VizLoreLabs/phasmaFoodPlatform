from django.contrib import admin
from .models import PlatformStatistic


@admin.register(PlatformStatistic)
class PlatformStatisticAdmin(admin.ModelAdmin):
    list_display = ("pk", "users", "platform")
    ordering = ("-date_created",)
    fieldsets = (
        ("Users", {"fields": ("users",)}),
        ("Platform", {"fields": ("platform",)}),
        ("Mongo", {"fields": ("mongo",)}),
        ("Postgres", {"fields": ("postgres",)}),
        ("Date created", {"fields": ("date_created",)}),
    )
    readonly_fields = ("date_created",)
    filter_horizontal = ()
