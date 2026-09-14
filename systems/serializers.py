"""
KD-HDIE Framework v1.0

Systems Serializers

Author:
Oybek Xolmuminov

Purpose:
Serialization and validation of external systems.
"""

from rest_framework import serializers

from .models import System


class SystemSerializer(serializers.ModelSerializer):
    """
    Serializer for System model.
    """

    class Meta:

        model = System

        fields = [

            "id",

            "system_name",

            "system_code",

            "description",

            "system_type",

            "communication_protocol",

            "base_url",

            "api_key",

            "username",

            "password",

            "database_name",

            "host",

            "port",

            "is_active",

            "created_at",

            "updated_at",

        ]

        read_only_fields = (

            "id",

            "created_at",

            "updated_at",

        )

        extra_kwargs = {

            "password": {

                "write_only": True

            }

        }

    # --------------------------------------------------

    # FIELD VALIDATION

    # --------------------------------------------------

    def validate_system_name(self, value):

        if len(value.strip()) < 3:

            raise serializers.ValidationError(

                "System name must contain at least 3 characters."

            )

        return value

    # --------------------------------------------------

    def validate_system_code(self, value):

        value = value.upper()

        if len(value) < 2:

            raise serializers.ValidationError(

                "System code is too short."

            )

        return value

    # --------------------------------------------------

    def validate_port(self, value):

        if value is None:

            return value

        if value < 1 or value > 65535:

            raise serializers.ValidationError(

                "Invalid port number."

            )

        return value

    # --------------------------------------------------

    # OBJECT VALIDATION

    # --------------------------------------------------

    def validate(self, attrs):

        protocol = attrs.get(

            "communication_protocol"

        )

        url = attrs.get(

            "base_url"

        )

        if protocol in [

            "REST",

            "SOAP",

            "GRAPHQL",

        ]:

            if not url:

                raise serializers.ValidationError({

                    "base_url":

                    "Base URL is required."

                })

        return attrs

    # --------------------------------------------------

    def create(self, validated_data):

        return System.objects.create(

            **validated_data

        )

    # --------------------------------------------------

    def update(

        self,

        instance,

        validated_data

    ):

        for key, value in validated_data.items():

            setattr(

                instance,

                key,

                value

            )

        instance.save()

        return instance
