# Generated by Django 2.2.2 on 2019-06-19 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0027_auto_20190619_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='varen_ID',
            new_name='emp_ID',
        ),
    ]
