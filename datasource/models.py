from django.db import models


class DataSource(models.Model):

    SOURCE_TYPES = (
        ("API", "API"),
        ("DATABASE", "Database"),
        ("CSV", "CSV"),
        ("EXCEL", "Excel"),
        ("JSON", "JSON"),
        ("XML", "XML"),
        ("SATELLITE", "Satellite"),
        ("SENSOR", "Sensor"),
        ("MANUAL", "Manual"),
    )

    system = models.ForeignKey(
        "systems.System",
        on_delete=models.CASCADE,
        related_name="data_sources",
        verbose_name="Tizim",
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Manba nomi",
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Kod",
    )

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        verbose_name="Manba turi",
    )

    endpoint = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Endpoint",
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ma'lumot manbasi"
        verbose_name_plural = "Ma'lumot manbalari"

    def __str__(self):
        return f"{self.system.name} - {self.name}"
