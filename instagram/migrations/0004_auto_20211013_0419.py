# Generated by Django 3.2.8 on 2021-10-13 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_auto_20211012_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='main_image',
            field=models.ImageField(null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(null=True, upload_to='image'),
        ),
    ]
