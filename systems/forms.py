from decimal import Decimal

from django import forms

from .models import System


class SystemForm(forms.ModelForm):
    """
    KD-HDIE Framework

    System Create / Update Form
    """

    class Meta:

        model = System

        exclude = (
            "id",
            "created_at",
            "updated_at",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "System name"
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Short code"
                }
            ),

            "organization": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "system_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "data_format": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "communication_protocol": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "authentication_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "api_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/api"
                }
            ),

            "language": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "timezone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "update_frequency": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "reliability_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "1"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def clean_code(self):
        """
        Kodni standart ko'rinishga keltirish.
        """

        code = self.cleaned_data["code"]

        return code.upper().strip()

    def clean_reliability_score(self):
        """
        Ishonchlilik koeffitsientini tekshirish.
        """

        score = self.cleaned_data["reliability_score"]

        if score < Decimal("0.00") or score > Decimal("1.00"):
            raise forms.ValidationError(
                "Reliability score 0.00 va 1.00 oralig'ida bo'lishi kerak."
            )

        return score

    def clean(self):
        """
        Qo'shimcha biznes qoidalari.
        """

        cleaned_data = super().clean()

        system_type = cleaned_data.get("system_type")
        api_url = cleaned_data.get("api_url")

        if system_type == "API" and not api_url:
            self.add_error(
                "api_url",
                "API turidagi tizim uchun API URL majburiy."
            )

        return cleaned_data
