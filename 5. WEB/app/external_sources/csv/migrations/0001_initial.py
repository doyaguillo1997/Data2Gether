# Generated by Django 3.2 on 2021-04-08 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField()),
                ('mapper', models.JSONField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyDirty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('load', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csv.load')),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='properties.property')),
            ],
            options={
                'verbose_name_plural': 'Dirty Properties',
            },
        ),
    ]
