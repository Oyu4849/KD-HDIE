from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Platformaning foydalanuvchi modeli.
    """

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefon raqami"
    )

    organization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Tashkilot"
    )

    position = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Lavozim"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.get_full_name() or self.username
