# Generated by Django 2.2.2 on 2019-06-18 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0008_auto_20190617_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(default='cat.jpg', upload_to=''),
        ),
    ]