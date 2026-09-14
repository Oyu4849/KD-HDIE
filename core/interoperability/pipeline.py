"""
KD-HDIE Framework v1.0

Pipeline Manager

Purpose:
Dynamic execution pipeline for heterogeneous
data integration algorithms.

Author:
Oybek Xolmuminov
"""

from integration.registry import AlgorithmRegistry


class PipelineManager:
    """
    Dynamic Algorithm Pipeline
    """

    def __init__(self):

        self.steps = []

    # --------------------------------------------------

    def add_step(
        self,
        algorithm_name,
        **kwargs,
    ):
        """
        Add algorithm into pipeline.
        """

        if not AlgorithmRegistry.exists(
            algorithm_name
        ):

            raise ValueError(
                f"Algorithm '{algorithm_name}' not found."
            )

        self.steps.append(

            {
                "name": algorithm_name,
                "params": kwargs,
            }

        )

    # --------------------------------------------------

    def clear(self):

        self.steps.clear()

    # --------------------------------------------------

    def count(self):

        return len(self.steps)

    # --------------------------------------------------

    def execute(
        self,
        data,
    ):
        """
        Execute all algorithms sequentially.
        """

        current = data

        for step in self.steps:

            algorithm_class = AlgorithmRegistry.get(

                step["name"]

            )

            params = step["params"]

            algorithm = algorithm_class(

                current,

                **params

            )

            current = algorithm.run()

        return current

    # --------------------------------------------------

    def get_steps(self):

        return [

            step["name"]

            for step in self.steps

        ]
