# Generated by Django 5.0 on 2023-12-25 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0003_orderinvestment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinvestment',
            name='product',
        ),
        migrations.AddField(
            model_name='orderinvestment',
            name='investment',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='imports.investment'),
        ),
    ]