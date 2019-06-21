# Generated by Django 2.2.2 on 2019-06-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='manager_email',
            field=models.EmailField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='picture',
            name='name',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='tempphoto',
            name='name',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]