"""
KD-HDIE Framework Result Provider

Provides live multi-source execution results
for the Django presentation layer.
"""

from datetime import date

from core.framework import KDHDIEFramework


class FrameworkResultProvider:

    @staticmethod
    def get():

        framework = KDHDIEFramework()

        # NASA POWER MONTHLY meteorological data
        # is available through the latest complete year.
        # Open-Meteo historical data is requested for
        # the same period so that both sources have
        # a common temporal domain for fusion.

        latest_complete_year = (
            date.today().year - 1
        )

        start_date = (
            f"{latest_complete_year}-01-01"
        )

        end_date = (
            f"{latest_complete_year}-12-31"
        )

        sources = [

            {
                "source_system": "OPENMETEO",

                "connection_parameters": {

                    "latitude": 45.0,

                    "longitude": 59.0,

                    "start_date": start_date,

                    "end_date": end_date,

                    "historical": True,

                },

            },

            {

                "source_system": "NASA",

                "connection_parameters": {

                    "latitude": 45.0,

                    "longitude": 59.0,

                    "start": start_date.replace("-", ""),

                    "end": end_date.replace("-", ""),

                    "temporal": "DAILY",

                    "parameters": [

                        "T2M",

                        "PRECTOTCORR",

                        "WS2M",

                    ],

                },

            },

        ]

        result = (
            framework.execute_multi_source(

                sources=sources,

                workflow="DAILY",

            )
        )

        return result.to_dict()
