import uuid
from decimal import Decimal

from django.db import models


class SystemType(models.TextChoices):
    API = "API", "API"
    DATABASE = "DATABASE", "Database"
    SATELLITE = "SATELLITE", "Satellite"
    SENSOR = "SENSOR", "Sensor"
    LABORATORY = "LABORATORY", "Laboratory"
    MANUAL = "MANUAL", "Manual"


class DataFormat(models.TextChoices):
    JSON = "JSON", "JSON"
    XML = "XML", "XML"
    CSV = "CSV", "CSV"
    EXCEL = "EXCEL", "Excel"
    GEOJSON = "GEOJSON", "GeoJSON"
    GEOTIFF = "GEOTIFF", "GeoTIFF"


class CommunicationProtocol(models.TextChoices):
    REST = "REST", "REST API"
    SOAP = "SOAP", "SOAP"
    FTP = "FTP", "FTP"
    MQTT = "MQTT", "MQTT"
    WEBSOCKET = "WEBSOCKET", "WebSocket"


class AuthenticationType(models.TextChoices):
    NONE = "NONE", "None"
    API_KEY = "API_KEY", "API Key"
    BASIC = "BASIC", "Basic Authentication"
    JWT = "JWT", "JWT"
    OAUTH2 = "OAUTH2", "OAuth2"


class UpdateFrequency(models.TextChoices):
    REALTIME = "REALTIME", "Real-time"
    HOURLY = "HOURLY", "Hourly"
    DAILY = "DAILY", "Daily"
    WEEKLY = "WEEKLY", "Weekly"
    MONTHLY = "MONTHLY", "Monthly"


class System(models.Model):
    """
    Tashqi axborot tizimlari modeli.

    Ushbu model KD-HDIE platformasiga ulanadigan barcha
    tashqi axborot tizimlari haqida metama'lumotlarni saqlaydi.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="System Name",
        help_text="Unique system name."
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="System Code",
        help_text="Unique short code."
    )

    organization = models.CharField(
        max_length=200,
        verbose_name="Organization"
    )

    system_type = models.CharField(
        max_length=30,
        choices=SystemType.choices,
        default=SystemType.API,
        verbose_name="System Type"
    )

    data_format = models.CharField(
        max_length=30,
        choices=DataFormat.choices,
        default=DataFormat.JSON,
        verbose_name="Data Format"
    )

    communication_protocol = models.CharField(
        max_length=30,
        choices=CommunicationProtocol.choices,
        default=CommunicationProtocol.REST,
        verbose_name="Communication Protocol"
    )

    authentication_type = models.CharField(
        max_length=30,
        choices=AuthenticationType.choices,
        default=AuthenticationType.NONE,
        verbose_name="Authentication Type"
    )

    api_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="API URL"
    )

    language = models.CharField(
        max_length=50,
        default="English",
        verbose_name="Language"
    )

    timezone = models.CharField(
        max_length=100,
        default="UTC",
        verbose_name="Time Zone"
    )

    update_frequency = models.CharField(
        max_length=30,
        choices=UpdateFrequency.choices,
        default=UpdateFrequency.DAILY,
        verbose_name="Update Frequency"
    )

    reliability_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("1.00"),
        verbose_name="Reliability Score",
        help_text="Value between 0.00 and 1.00"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        db_table = "systems"

        ordering = ["name"]

        verbose_name = "System"

        verbose_name_plural = "Systems"

    def __str__(self):
        return f"{self.name} ({self.code})"
