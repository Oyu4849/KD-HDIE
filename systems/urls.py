"""
KD-HDIE Framework

Systems URL Configuration

Scientific Platform Routing

Author:
KD-HDIE Framework
"""

from django.urls import path

from . import views


app_name = "systems"


urlpatterns = [

    # ==========================================================
    # Dashboard
    # ==========================================================

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # ==========================================================
    # Execute Framework - CSV
    # ==========================================================

    path(
        "execute/",
        views.execute_framework,
        name="execute",
    ),

    # ==========================================================
    # Execute Open-Meteo
    # ==========================================================

    path(
        "execute-openmeteo/",
        views.execute_openmeteo,
        name="execute_openmeteo",
    ),

    # ==========================================================
    # Execute NASA POWER
    # ==========================================================

    path(
        "execute-nasa/",
        views.execute_nasa,
        name="execute_nasa",
    ),

    # ==========================================================
    # Execute Generic REST/JSON API
    # ==========================================================

    path(
        "execute-generic-api/",
        views.execute_generic_api,
        name="execute_generic_api",
    ),

    path(
        "execute-multi-source/",
        views.execute_multi_source,
        name="execute_multi_source",
    ),
    # ==========================================================
    # Metadata Explorer
    # ==========================================================

    path(
        "metadata/",
        views.metadata_explorer,
        name="metadata",
    ),

    # ==========================================================
    # Interoperability Explorer
    # ==========================================================

    path(
        "interoperability/",
        views.interoperability_explorer,
        name="interoperability",
    ),

    # ==========================================================
    # Knowledge Graph
    # ==========================================================

    path(
        "knowledge-graph/",
        views.knowledge_graph,
        name="knowledge-graph",
    ),

    # ==========================================================
    # Processing Pipeline
    # ==========================================================

    path(
        "pipeline/",
        views.pipeline,
        name="pipeline",
    ),

    # ==========================================================
    # Algorithm Monitor
    # ==========================================================

    path(
        "algorithm-monitor/",
        views.algorithm_monitor,
        name="algorithm_monitor",
    ),

    # ==========================================================
    # Framework Analytics
    # ==========================================================

    path(
        "analytics/",
        views.framework_statistics,
        name="analytics",
    ),

    # ==========================================================
    # Quality Dashboard
    # ==========================================================

    path(
        "quality/",
        views.quality_dashboard,
        name="quality",
    ),

    # ==========================================================
    # Conflict Analysis
    # ==========================================================

    path(
        "conflicts/",
        views.conflict_analysis,
        name="conflicts",
    ),

    # ==========================================================
    # Fusion Results
    # ==========================================================

    path(
        "fusion/",
        views.fusion_results,
        name="fusion",
    ),

    # ==========================================================
    # Unified Information Model
    # ==========================================================

    path(
        "unified-model/",
        views.unified_model,
        name="unified-model",
    ),

    # ==========================================================
    # Scientific Reports
    # ==========================================================

    path(
        "reports/",
        views.reports,
        name="reports",
    ),

]
