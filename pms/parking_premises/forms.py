from django import forms
from parking_premises.models import Premises, Slot


class CreatePremiseForm(forms.ModelForm):
    class Meta:
        model = Premises

        fields = ["premise_name", "address", "authorized_person_name", "authorized_person_contact"]
        widgets = {
            "premise_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter premise name",
                    "aria-invalid": "true",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "aria-invalid": "true",
                    "placeholder": "Enter address",
                }
            ),
            "authorized_person_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter authorized person name",
                    "aria-invalid": "true",
                }
            ),
            "authorized_person_contact": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter authorized person contact",
                    "aria-invalid": "true",
                }
            ),
        }


class CreateSlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ["premise_slot", "vehicle_type", "price"]
        widgets = {
            "premise_slot": forms.Select(
                attrs={
                    "class": "form-control",
                    "aria-invalid": "true",
                }
            ),
            "vehicle_type": forms.Select(
                attrs={
                    "class": "form-control",
                    "aria-invalid": "true",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter price",
                    "aria-invalid": "true",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CreateSlotForm, self).__init__(*args, **kwargs)
        self.fields["premise_slot"].queryset = Premises.objects.all()


