# Generated by Django 3.2.6 on 2021-09-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastres', '0002_auto_20210603_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Nombre de la via')),
            ],
        ),
    ]
