# Generated by Django 3.2.6 on 2021-08-24 09:06

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_cole', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='lat',
            field=models.FloatField(default=-1, verbose_name='Lat'),
        ),
        migrations.AddField(
            model_name='school',
            name='lon',
            field=models.FloatField(default=-1, verbose_name='lon'),
        ),
        migrations.AlterField(
            model_name='school',
            name='coord',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Localización'),
        ),
    ]
