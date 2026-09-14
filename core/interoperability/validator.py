"""
KD-HDIE Framework

Interoperability Validator

Purpose:
Validate heterogeneous data before interoperability
processing starts.

Dissertation:
Chapter 3
Interoperability Validation Stage

Author:
Oybek Xolmuminov
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationError:

    field: str

    message: str


@dataclass
class ValidationResult:

    valid: bool = True

    errors: list[ValidationError] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    def add_error(self, field: str, message: str):

        self.valid = False

        self.errors.append(

            ValidationError(

                field=field,

                message=message

            )

        )

    def add_warning(self, message: str):

        self.warnings.append(message)


class InteroperabilityValidator:
    """
    Validates heterogeneous datasets before
    interoperability processing.
    """

    REQUIRED_KEYS = (
        "attribute",
        "value",
    )

    def validate(self, records: list[dict]) -> ValidationResult:

        result = ValidationResult()

        if not isinstance(records, list):

            result.add_error(
                "records",
                "Input data must be a list."
            )

            return result

        if len(records) == 0:

            result.add_warning(
                "Dataset is empty."
            )

            return result

        for index, record in enumerate(records):

            if not isinstance(record, dict):

                result.add_error(

                    f"record[{index}]",

                    "Record must be a dictionary."

                )

                continue

            for key in self.REQUIRED_KEYS:

                if key not in record:

                    result.add_error(

                        f"record[{index}].{key}",

                        "Required field is missing."

                    )

            value = record.get("value")

            if value is None:

                result.add_warning(

                    f"record[{index}] contains NULL value."

                )

        return result
