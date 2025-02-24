from django import forms
from .models import NutritionalInfo


class NutritionalInfoForm(forms.ModelForm):
    class Meta:
        model = NutritionalInfo
        fields = ["protein", "carb", "fat", "calories"]
        widgets = {
            "protein": forms.NumberInput(attrs={"class": "w-full py-2 px-4 rounded-xl"}),
            "carb": forms.NumberInput(attrs={"class": "w-full py-2 px-4 rounded-xl"}),
            "fat": forms.NumberInput(attrs={"class": "w-full py-2 px-4 rounded-xl"}),
            "calories": forms.NumberInput(attrs={"class": "w-full py-2 px-4 rounded-xl"}),
        }
