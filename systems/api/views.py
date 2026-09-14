"""
KD-HDIE Framework

Systems API Views

Scientific REST API Layer

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from systems.models import System
from systems.serializers import SystemSerializer
from systems.services import SystemService

#from core.interoperability.controller import InteroperabilityController


def knowledge_graph_api(request):
    """
    Return Knowledge Graph JSON.
    """

    context = SystemService.get_knowledge_graph_context()

    return JsonResponse(
        {
            "success": True,
            "data": {
                "nodes": context.get("nodes", []),
                "edges": context.get("edges", []),
            },
        }
    )

# ==========================================================
# Base API View
# ==========================================================

class BaseAPIView(APIView):
    """
    Base API View for KD-HDIE Framework.
    Provides common helper methods.
    """

    @staticmethod
    def success(data, http_status=status.HTTP_200_OK):
        return Response(
            {
                "success": True,
                "data": data,
            },
            status=http_status,
        )

    @staticmethod
    def error(message, http_status=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "success": False,
                "message": message,
            },
            status=http_status,
        )


# ==========================================================
# System List API
# ==========================================================

class SystemListAPIView(BaseAPIView):
    """
    Return all registered systems.
    """

    def get(self, request):

        systems = SystemService.get_all_systems()

        serializer = SystemSerializer(
            systems,
            many=True,
        )

        return self.success(serializer.data)


# ==========================================================
# System Detail API
# ==========================================================

class SystemDetailAPIView(BaseAPIView):
    """
    Return system details.
    """

    def get(self, request, pk):

        try:

            system = System.objects.get(pk=pk)

        except System.DoesNotExist:

            return self.error(
                "System not found.",
                status.HTTP_404_NOT_FOUND,
            )

        serializer = SystemSerializer(system)

        return self.success(serializer.data)


# ==========================================================
# Integration API
# ==========================================================

class IntegrationAPIView(BaseAPIView):
    """
    Execute complete KD-HDIE integration workflow.
    """

    def post(self, request):

        connector = request.data.get("connector")

        endpoint = request.data.get("endpoint")

        params = request.data.get(
            "params",
            {},
        )

        reference_attributes = request.data.get(
            "reference_attributes",
            [],
        )

        if not connector:

            return self.error(
                "Connector is required."
            )

        controller = InteroperabilityController()

        result = controller.execute(

            connector_name=connector,

            reference_attributes=reference_attributes,

            endpoint=endpoint,

            params=params,

        )

        return self.success(result)

# ==========================================================
# Framework Statistics API
# ==========================================================

class FrameworkStatisticsAPIView(BaseAPIView):
    """
    Return KD-HDIE Framework execution statistics.
    """

    def get(self, request):

        statistics = SystemService.get_framework_statistics()

        return self.success(statistics)


# ==========================================================
# Metadata List API
# ==========================================================

class MetadataAPIView(BaseAPIView):
    """
    Return all canonical metadata attributes.
    """

    def get(self, request):

        context = SystemService.get_metadata_context()

        return self.success(
            context.get(
                "attributes",
                [],
            )
        )


# ==========================================================
# Metadata Detail API
# ==========================================================

class MetadataDetailAPIView(BaseAPIView):
    """
    Return metadata information for one canonical attribute.
    """

    def get(self, request, attribute):

        context = SystemService.get_metadata_context()

        attributes = context.get(
            "attributes",
            [],
        )

        for item in attributes:

            if item["key"] == attribute:

                return self.success(item)

        return self.error(

            "Attribute not found.",

            status.HTTP_404_NOT_FOUND,

        )


# ==========================================================
# Framework Summary API
# ==========================================================

class FrameworkSummaryAPIView(BaseAPIView):
    """
    Return complete framework execution result.
    """

    def get(self, request):

        framework = SystemService.get_framework_result()

        return self.success(framework)
# ==========================================================
# Knowledge Graph API
# ==========================================================

class KnowledgeGraphAPIView(BaseAPIView):
    """
    Knowledge Graph API
    """

    def get(self, request):

        context = SystemService.get_knowledge_graph_context()

        nodes = []

        edges = []

        #
        # Domain Nodes
        #

        for domain in context["domains"]:

            nodes.append({

                "id": domain,

                "label": domain,

                "group": "Domain",

                "shape": "box",

            })

        #
        # Attribute Nodes
        #

        for attribute in context["attributes"]:

            nodes.append({

                "id": attribute["key"],

                "label": attribute["label"],

                "group": attribute["domain"],

                "shape": "dot",

            })

            edges.append({

                "from": attribute["domain"],

                "to": attribute["key"],

            })

        return self.success({

            "nodes": nodes,

            "edges": edges,

        })

# ==========================================================
# Quality API
# ==========================================================

class QualityAPIView(BaseAPIView):
    """
    Return framework quality statistics.
    """

    def get(self, request):

        statistics = SystemService.get_framework_statistics()

        return self.success({

            "quality_score":
                statistics.get("quality_score", 0),

            "completeness":
                statistics.get("completeness", 0),

            "validity":
                statistics.get("validity", 0),

            "valid_attributes":
                statistics.get("valid_attributes", 0),

            "missing_values":
                statistics.get("missing_values", 0),

        })


# ==========================================================
# Conflict API
# ==========================================================

class ConflictAPIView(BaseAPIView):
    """
    Return conflict analysis statistics.
    """

    def get(self, request):

        statistics = SystemService.get_framework_statistics()

        return self.success({

            "conflicts":
                statistics.get("conflicts", 0),

            "duplicate_groups":
                statistics.get("duplicate_groups", 0),

            "value_conflicts":
                statistics.get("value_conflicts", 0),

            "unit_conflicts":
                statistics.get("unit_conflicts", 0),

            "conflict_rate":
                statistics.get("conflict_rate", 0),

        })


# ==========================================================
# Fusion API
# ==========================================================

class FusionAPIView(BaseAPIView):
    """
    Return fusion statistics.
    """

    def get(self, request):

        statistics = SystemService.get_framework_statistics()

        return self.success({

            "input_records":
                statistics.get("input_records", 0),

            "fused_records":
                statistics.get("fused_records", 0),

            "fusion_groups":
                statistics.get("fusion_groups", 0),

            "final_records":
                statistics.get("final_records", 0),

        })


# ==========================================================
# Unified Information Model API
# ==========================================================

class UnifiedModelAPIView(BaseAPIView):
    """
    Return Unified Information Model statistics.
    """

    def get(self, request):

        statistics = SystemService.get_framework_statistics()

        return self.success({

            "records":
                statistics.get("records", 0),

            "canonical_attributes":
                statistics.get("canonical_attributes", 0),

            "resolved_attributes":
                statistics.get("resolved_attributes", 0),

            "framework_version":
                statistics.get("framework_version", ""),

            "workflow":
                statistics.get("workflow", ""),

            "source_system":
                statistics.get("source_system", ""),

            "target_system":
                statistics.get("target_system", ""),

        })
