# Generated by Django 3.2.8 on 2021-10-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='create_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='update_date',
            field=models.DateTimeField(null=True),
        ),
    ]
