# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-19 21:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180419_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]