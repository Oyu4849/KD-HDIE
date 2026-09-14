"""
KD-HDIE Framework

Systems API URL Configuration
Scientific REST API
"""

from django.urls import path

from .views import (
    SystemListAPIView,
    SystemDetailAPIView,
    IntegrationAPIView,
    FrameworkSummaryAPIView,
    FrameworkStatisticsAPIView,
    MetadataAPIView,
    MetadataDetailAPIView,
    KnowledgeGraphAPIView,
    QualityAPIView,
    ConflictAPIView,
    FusionAPIView,
    UnifiedModelAPIView,
)

app_name = "systems_api"

urlpatterns = [

    # ==========================================================
    # System Management
    # ==========================================================

    path(
        "",
        SystemListAPIView.as_view(),
        name="system-list",
    ),

    path(
        "<int:pk>/",
        SystemDetailAPIView.as_view(),
        name="system-detail",
    ),

    # ==========================================================
    # Framework Execution
    # ==========================================================

    #path(
    #    "integration/",
    #    IntegrationAPIView.as_view(),
    #    name="integration",
    #),

    path(
        "framework/",
        FrameworkSummaryAPIView.as_view(),
        name="framework",
    ),

    path(
        "statistics/",
        FrameworkStatisticsAPIView.as_view(),
        name="statistics",
    ),

    # ==========================================================
    # Metadata Explorer
    # ==========================================================

    path(
        "metadata/",
        MetadataAPIView.as_view(),
        name="metadata",
    ),

    path(
        "metadata/<str:attribute>/",
        MetadataDetailAPIView.as_view(),
        name="metadata-detail",
    ),

    # ==========================================================
    # Knowledge Graph
    # ==========================================================

    path(
        "knowledge-graph/",
        KnowledgeGraphAPIView.as_view(),
        name="knowledge-graph",
    ),

    # ==========================================================
    # Data Quality
    # ==========================================================

    path(
        "quality/",
        QualityAPIView.as_view(),
        name="quality",
    ),

    # ==========================================================
    # Conflict Analysis
    # ==========================================================

    path(
        "conflicts/",
        ConflictAPIView.as_view(),
        name="conflicts",
    ),

    # ==========================================================
    # Data Fusion
    # ==========================================================

    path(
        "fusion/",
        FusionAPIView.as_view(),
        name="fusion",
    ),

    # ==========================================================
    # Unified Information Model
    # ==========================================================

    path(
        "unified-model/",
        UnifiedModelAPIView.as_view(),
        name="unified-model",
    ),

]
