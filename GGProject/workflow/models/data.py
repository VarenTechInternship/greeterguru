import .models

e  = Employee(
        first_name = 'Caroline',
        last_name = 'Orndorff',
        emp_email = 'orndorffc@varentech.com',
        manager_email = 'orndorffc@varentech.com',
        keycode = 12345,
        emp_ID = '1',
        emp_permissions = '1',
    )
e.save()
