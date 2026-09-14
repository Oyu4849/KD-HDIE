"""
KD-HDIE Framework

System Views
Final v3.0

Scientific Presentation Layer

Responsibilities
----------------
• Dashboard presentation
• Single-source framework execution
• Multi-source framework execution
• Metadata Explorer
• Knowledge Graph
• Interoperability Explorer
• Processing Pipeline
• Algorithm Monitor
• Framework Analytics
• Quality Dashboard
• Conflict Analysis
• Fusion Results
• Unified Model
• Scientific Reports

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

import json
from typing import Any

from django.http import JsonResponse
from django.shortcuts import render

from core.framework import KDHDIEFramework

from .services import SystemService
from django.views.decorators.csrf import csrf_exempt

# ==========================================================
# Internal Framework Helper
# ==========================================================

def _execute_framework(
    source_system: str = "CSV",
    connection_parameters: dict[str, Any] | None = None,
):
    """
    Execute KD-HDIE Framework for a single source system.

    Supported source systems:
        CSV
        OPENMETEO
        NASA
    """

    framework = KDHDIEFramework()

    if connection_parameters is None:
        connection_parameters = {}

    result = framework.execute(

        source_system=source_system,

        target_system="KD-HDIE",

        workflow="DEFAULT",

        connection_parameters=(
            connection_parameters
        ),

    )

    return result.to_dict()


# ==========================================================
# Dashboard
# ==========================================================

def dashboard(request):
    """
    Scientific Dashboard.
    """

    context = (
        SystemService
        .get_dashboard_context()
    )

    return render(

        request,

        "systems/dashboard.html",

        context,

    )


# ==========================================================
# Execute Framework - CSV
# ==========================================================

def execute_framework(request):
    """
    Execute complete KD-HDIE workflow
    using CSV source.
    """

    payload = _execute_framework(

        source_system="CSV",

        connection_parameters={

            "file_path":
                "media/aral_monthly_heterogeneous_2017_2025.csv",

        },

    )

    if "application/json" in request.headers.get(
        "Accept",
        "",
    ):

        return JsonResponse(

            payload,

            safe=False,

        )

    context = (
        SystemService
        .get_dashboard_context()
    )

    return render(

        request,

        "systems/dashboard.html",

        context,

    )


# ==========================================================
# Execute Open-Meteo Historical
# ==========================================================

def execute_openmeteo(request):
    """
    Execute KD-HDIE workflow using
    Open-Meteo historical weather data.

    Historical period:
        2025-01-01
        2025-12-31
    """

    connection_parameters = {

        "latitude": 45.0,

        "longitude": 59.0,

        "start_date": "2025-01-01",

        "end_date": "2025-12-31",

        "historical": True,

    }

    payload = _execute_framework(

        source_system="OPENMETEO",

        connection_parameters=(
            connection_parameters
        ),

    )

    return JsonResponse(

        payload,

        safe=False,

    )


# ==========================================================
# Execute NASA POWER
# ==========================================================

def execute_nasa(request):
    """
    Execute KD-HDIE workflow using
    NASA POWER monthly data.

    Parameters:
        T2M
        PRECTOTCORR
        RH2M
        WS2M
    """

    connection_parameters = {

        "latitude": 45.0,

        "longitude": 59.0,

        "start": "2025",

        "end": "2025",

        "parameters": [

            "T2M",

            "PRECTOTCORR",

            "RH2M",

            "WS2M",

        ],

    }

    payload = _execute_framework(

        source_system="NASA",

        connection_parameters=(
            connection_parameters
        ),

    )

    return JsonResponse(

        payload,

        safe=False,

    )

# ==========================================================
# Execute Generic REST/JSON API
# ==========================================================

@csrf_exempt
def execute_generic_api(request):
    """
    Execute KD-HDIE workflow using a runtime-configured
    generic REST/JSON API.

    Expected POST body:

    {
        "url": "https://example.com/api/data",
        "method": "GET",
        "params": {
            "latitude": 45.0,
            "longitude": 59.0
        },
        "headers": {}
    }
    """

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Generic API execution requires "
                    "an HTTP POST request."
                ),
            },
            status=405,
        )

    # ======================================================
    # Parse JSON
    # ======================================================

    try:

        body = request.body.decode("utf-8")

        data = json.loads(body) if body.strip() else {}

    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid JSON request body.",
            },
            status=400,
        )

    # ======================================================
    # API Configuration
    # ======================================================

    url = str(
        data.get("url", "")
    ).strip()

    method = str(
        data.get("method", "GET")
    ).upper().strip()

    params = data.get(
        "params",
        {},
    )

    headers = data.get(
        "headers",
        {},
    )

    json_body = data.get(
        "json",
        None,
    )

    # ======================================================
    # Validation
    # ======================================================

    if not url:

        return JsonResponse(
            {
                "success": False,
                "message": "API URL is required.",
            },
            status=400,
        )

    if method not in {
        "GET",
        "POST",
    }:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Unsupported HTTP method. "
                    "Supported methods: GET, POST."
                ),
            },
            status=400,
        )

    if not isinstance(params, dict):

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "API parameters must be "
                    "a JSON object."
                ),
            },
            status=400,
        )

    if not isinstance(headers, dict):

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "API headers must be "
                    "a JSON object."
                ),
            },
            status=400,
        )

    # ======================================================
    # Framework Execution
    # ======================================================

    connection_parameters = {

        "url": url,

        "method": method,

        "params": params,

        "headers": headers,

        "json": json_body,

    }

    payload = _execute_framework(

        source_system="GENERIC_API",

        connection_parameters=(
            connection_parameters
        ),

    )

    return JsonResponse(
        payload,
        safe=False,
    )

# ==========================================================
# Execute Multi-Source
# ==========================================================
@csrf_exempt
def execute_multi_source(request):
    """
    Execute KD-HDIE interoperability workflow
    using multiple heterogeneous data sources.

    Sources
    -------
    1. Open-Meteo
    2. NASA POWER

    Default spatial parameters:
        latitude  = 45.0
        longitude = 59.0

    Default period:
        2025

    Processing
    ----------
    Each source is independently processed through
    source-level normalization, semantic mapping,
    harmonization and monthly aggregation.

    The resulting source datasets are then merged
    and passed to:

        Quality
            ↓
        Conflict
            ↓
        Reliability
            ↓
        Fusion
            ↓
        UnifiedModel
    """

    framework = KDHDIEFramework()

    # ======================================================
    # Default Parameters
    # ======================================================

    openmeteo_parameters = {

        "latitude": 45.0,

        "longitude": 59.0,

        "start_date": "2025-01-01",

        "end_date": "2025-12-31",

        "historical": True,

    }

    nasa_parameters = {

        "latitude": 45.0,

        "longitude": 59.0,

        "start": "2025",

        "end": "2025",

        "parameters": [

            "T2M",

            "PRECTOTCORR",

            "RH2M",

            "WS2M",

        ],

    }

    # ======================================================
    # Optional JSON Request Body
    # ======================================================
    #
    # POST requests may provide:
    #
    # {
    #     "latitude": 45.0,
    #     "longitude": 59.0,
    #     "year": 2025
    # }
    #
    # If parsing fails, defaults remain active.
    # ======================================================

    if request.method == "POST":

        try:

            body = request.body.decode(
                "utf-8"
            )

            if body.strip():

                data = json.loads(body)

                latitude = float(
                    data.get(
                        "latitude",
                        45.0,
                    )
                )

                longitude = float(
                    data.get(
                        "longitude",
                        59.0,
                    )
                )

                year = int(
                    data.get(
                        "year",
                        2025,
                    )
                )

                start_date = (
                    f"{year}-01-01"
                )

                end_date = (
                    f"{year}-12-31"
                )

                openmeteo_parameters = {

                    "latitude":
                        latitude,

                    "longitude":
                        longitude,

                    "start_date":
                        start_date,

                    "end_date":
                        end_date,

                    "historical":
                        True,

                }

                nasa_parameters = {

                    "latitude":
                        latitude,

                    "longitude":
                        longitude,

                    "start":
                        str(year),

                    "end":
                        str(year),

                    "parameters": [

                        "T2M",

                        "PRECTOTCORR",

                        "RH2M",

                        "WS2M",

                    ],

                }

        except (
            ValueError,
            TypeError,
            json.JSONDecodeError,
        ):

            # Keep validated default parameters.
            pass

    # ======================================================
    # Multi-Source Definition
    # ======================================================

    sources = [

        {

            "source_system":
                "OPENMETEO",

            "connection_parameters":
                openmeteo_parameters,

        },

        {

            "source_system":
                "NASA",

            "connection_parameters":
                nasa_parameters,

        },

    ]

    # ======================================================
    # Execute Multi-Source Framework
    # ======================================================

    result = framework.execute_multi_source(

        sources=sources,

        workflow="DEFAULT",

    )

    # ======================================================
    # JSON Response
    # ======================================================

    return JsonResponse(

        result.to_dict(),

        safe=False,

    )


# ==========================================================
# Metadata Explorer
# ==========================================================

def metadata_explorer(request):
    """
    Scientific Metadata Explorer.
    """

    context = (
        SystemService
        .get_metadata_context()
    )

    return render(

        request,

        "systems/metadata_explorer.html",

        context,

    )


# ==========================================================
# Knowledge Graph
# ==========================================================

def knowledge_graph(request):
    """
    Scientific Knowledge Graph.
    """

    context = (
        SystemService
        .get_knowledge_graph_context()
    )

    return render(

        request,

        "systems/knowledge_graph.html",

        context,

    )


# ==========================================================
# Algorithm Execution Monitor
# ==========================================================

def algorithm_monitor(request):
    """
    Scientific Algorithm Execution Monitor.
    """

    context = (
        SystemService
        .get_algorithm_monitor_context()
    )

    return render(

        request,

        "systems/algorithm_monitor.html",

        context,

    )


# ==========================================================
# Interoperability Explorer
# ==========================================================

def interoperability_explorer(request):
    """
    Scientific Interoperability Explorer.
    """

    context = {

        "statistics":
            SystemService
            .get_framework_statistics(),

        "metadata":
            SystemService
            .get_framework_metadata(),

        "overview":
            SystemService
            .get_system_overview(),

    }

    return render(

        request,

        "systems/interoperability_explorer.html",

        context,

    )


# ==========================================================
# Processing Pipeline
# ==========================================================

def pipeline(request):
    """
    KD-HDIE Processing Pipeline.
    """

    context = (
        SystemService
        .get_algorithm_monitor_context()
    )

    return render(

        request,

        "systems/pipeline.html",

        context,

    )


# ==========================================================
# Framework Status
# ==========================================================

def framework_status(request):
    """
    Return framework execution status.
    """

    return JsonResponse(

        SystemService
        .get_framework_health(),

        safe=False,

    )


# ==========================================================
# Dashboard Metrics
# ==========================================================

def dashboard_metrics(request):
    """
    Dashboard metrics endpoint.
    """

    return JsonResponse(

        SystemService
        .get_dashboard_metrics(),

        safe=False,

    )


# ==========================================================
# System Overview
# ==========================================================

def system_overview(request):
    """
    Framework overview endpoint.
    """

    return JsonResponse(

        SystemService
        .get_system_overview(),

        safe=False,

    )


# ==========================================================
# Framework Statistics
# ==========================================================

def framework_statistics(request):
    """
    Return framework statistics.
    """

    return JsonResponse(

        SystemService
        .get_framework_statistics(),

        safe=False,

    )


# ==========================================================
# Framework Metadata
# ==========================================================

def framework_metadata(request):
    """
    Return framework metadata.
    """

    return JsonResponse(

        SystemService
        .get_framework_metadata(),

        safe=False,

    )


# ==========================================================
# Quality Dashboard
# ==========================================================

def quality_dashboard(request):
    """
    Quality assessment dashboard.
    """

    return render(

        request,

        "systems/quality_dashboard.html",

        {},

    )


# ==========================================================
# Conflict Analysis
# ==========================================================

def conflict_analysis(request):
    """
    Conflict detection and analysis.
    """

    return render(

        request,

        "systems/conflict_analysis.html",

        {},

    )


# ==========================================================
# Fusion Results
# ==========================================================

def fusion_results(request):
    """
    Data fusion results.
    """

    return render(

        request,

        "systems/fusion_results.html",

        {},

    )


# ==========================================================
# Unified Model
# ==========================================================

def unified_model(request):
    """
    Unified data model view.
    """

    return render(

        request,

        "systems/unified_model.html",

        {},

    )


# ==========================================================
# Reports
# ==========================================================

def reports(request):
    """
    Scientific reports.
    """

    return render(

        request,

        "systems/reports.html",

        {},

    )
