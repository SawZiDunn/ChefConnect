from django import forms
from .models import NutritionalInfo


class NutritionalInfoForm(forms.ModelForm):
    class Meta:
        model = NutritionalInfo
        fields = ["protein", "carb", "fat", "calories"]
        widgets = {
            "protein": forms.NumberInput(attrs={"class": "form-control"}),
            "carb": forms.NumberInput(attrs={"class": "form-control"}),
            "fat": forms.NumberInput(attrs={"class": "form-control"}),
            "calories": forms.NumberInput(attrs={"class": "form-control"}),
        }
