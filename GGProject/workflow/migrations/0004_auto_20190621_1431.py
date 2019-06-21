# Generated by Django 2.2.2 on 2019-06-21 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_auto_20190621_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_ID',
            field=models.IntegerField(null=True, unique=True, verbose_name='Employee ID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_permissions',
            field=models.CharField(choices=[(0, 'Never'), (1, 'Sometimes'), (2, 'Always')], default=0, max_length=15, verbose_name='Employee Permissions'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='keycode',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='manager_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='tempphoto',
            name='unknown_photo',
            field=models.ImageField(null=True, upload_to='TempPhotos/'),
        ),
    ]