# Generated by Django 2.2.2 on 2019-06-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0009_auto_20190618_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(default='cat.jpg', upload_to='Dataset'),
        ),
    ]
