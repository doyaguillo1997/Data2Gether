# Generated by Django 3.2.6 on 2021-08-24 07:56

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(verbose_name='Tipo')),
            ],
        ),
        migrations.CreateModel(
            name='GoogleElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Nombre')),
                ('rating', models.FloatField(verbose_name='Valoración')),
                ('user_ratings_total', models.IntegerField(verbose_name='Número valoraciones')),
                ('coord', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Localización')),
                ('price_level_missing', models.BinaryField(verbose_name='Falta Precio')),
                ('price_level', models.IntegerField(verbose_name='Nivel Precio')),
                ('price_level_weights', models.FloatField(verbose_name='Peso Precio')),
                ('find_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='places.googletype')),
            ],
        ),
    ]
