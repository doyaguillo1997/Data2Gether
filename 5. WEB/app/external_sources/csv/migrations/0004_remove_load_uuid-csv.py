# Generated by Django 3.2.4 on 2021-06-20 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csv', '0003_alter_load_uuid-csv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='load',
            name='UUID-CSV',
        ),
    ]