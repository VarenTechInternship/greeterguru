# Generated by Django 2.2.2 on 2019-06-17 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_auto_20190617_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(default='cat.jpg', upload_to='../FaceID/Dataset/'),
        ),
    ]
