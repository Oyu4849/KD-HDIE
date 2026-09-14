from django.contrib import admin

from .models import DataSource


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "system",
        "source_type",
        "is_active",
    )

    list_filter = (
        "system",
        "source_type",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )
