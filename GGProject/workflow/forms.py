from django.contrib.auth.forms import UserCreationForm
from .models import Employee


# Custom form for adding new employee through site
class EmployeeCreationForm(UserCreationForm):

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
