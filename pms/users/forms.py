from django import forms

from users.models import UserMaster


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = UserMaster

        fields = ["email", "user_type", "password"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email",
                    "aria-invalid": "true",
                }
            ),
            "user_type": forms.Select(
                attrs={
                    "class": "form-control",
                    "aria-invalid": "true",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter password",
                    "aria-invalid": "true",
                }
            ),
        }

    def save(self, commit=True):
        password = self.cleaned_data.get("password")
        instance = super(CreateUserForm, self).save(commit=False)
        instance.set_password(password)
        instance.save()
        return super(CreateUserForm, self).save(commit=commit)


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )
