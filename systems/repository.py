"""
KD-HDIE Framework

System Repository

Author:
Oybek Xolmuminov
"""

from django.db.models import QuerySet

from .models import System


class SystemRepository:
    """
    Repository layer for System model.
    """

    @staticmethod
    def all() -> QuerySet:
        """
        Return all systems.
        """
        return System.objects.all()

    @staticmethod
    def active() -> QuerySet:
        """
        Return active systems.
        """
        return System.objects.filter(
            is_active=True
        )

    @staticmethod
    def get(pk: int):

        return System.objects.filter(
            pk=pk
        ).first()

    @staticmethod
    def create(**data):

        return System.objects.create(
            **data
        )

    @staticmethod
    def update(system, **data):

        for key, value in data.items():

            setattr(
                system,
                key,
                value
            )

        system.save()

        return system

    @staticmethod
    def delete(system):

        system.delete()

    @staticmethod
    def search(keyword):

        return System.objects.filter(

            system_name__icontains=keyword

        )
