from django import forms
import re

from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must contain 8 characters."
            )

        if not re.match(r"^[A-Z]{3}", license_number):
            raise forms.ValidationError(
                "The first 3 characters must be uppercase letters."
            )

        if not re.match(r"^\d{5}$", license_number[3:]):
            raise forms.ValidationError(
                "The last 5 characters must be digits."
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
