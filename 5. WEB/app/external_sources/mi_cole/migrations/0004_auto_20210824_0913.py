# Generated by Django 3.2.6 on 2021-08-24 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_cole', '0003_auto_20210824_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='latitude',
            field=models.FloatField(default=-1, verbose_name='Lat'),
        ),
        migrations.AddField(
            model_name='school',
            name='longitude',
            field=models.FloatField(default=-1, verbose_name='lon'),
        ),
    ]
