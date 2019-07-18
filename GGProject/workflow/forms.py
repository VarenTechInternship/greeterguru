from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee


# Custom form for adding new employee through site
class EmployeeForm(forms.ModelForm):

    # Multiple password fields to use for verification
    password1 = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput,
        help_text = "Required. Secure password."
    )
    password2 = forms.CharField(
        label = "Password confirmation",
        widget = forms.PasswordInput,
        help_text = "Required. Password matching above entry."
    )

    class Meta:
        model = Employee
        fields = (
            'username',
            'password',
            'is_superuser',
            'is_staff',
            'first_name',
            'last_name',
            'email',
            'emp_ID',
            'keycode',
            'permissions',
        )

    # Check that the two password entries match
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    # Save the provided password in hashed format
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
