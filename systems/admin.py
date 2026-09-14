from django.contrib import admin

from .models import System


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    """
    KD-HDIE Framework
    System Administration Panel
    """

    # --------- List Page ---------

    list_display = (
        "name",
        "code",
        "system_type",
        "organization",
        "data_format",
        "communication_protocol",
        "update_frequency",
        "reliability_score",
        "is_active",
    )

    list_display_links = (
        "name",
        "code",
    )

    list_editable = (
        "is_active",
        "reliability_score",
    )

    list_filter = (
        "system_type",
        "data_format",
        "communication_protocol",
        "authentication_type",
        "update_frequency",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "organization",
        "description",
    )

    ordering = (
        "name",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    # --------- Detail Page ---------

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Asosiy ma'lumotlar",
            {
                "fields": (
                    "id",
                    "name",
                    "code",
                    "organization",
                    "description",
                )
            },
        ),

        (
            "Tizim parametrlari",
            {
                "fields": (
                    "system_type",
                    "data_format",
                    "communication_protocol",
                    "authentication_type",
                )
            },
        ),

        (
            "Integratsiya sozlamalari",
            {
                "fields": (
                    "api_url",
                    "language",
                    "timezone",
                    "update_frequency",
                    "reliability_score",
                )
            },
        ),

        (
            "Holati",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # --------- Save ---------

    save_on_top = True
