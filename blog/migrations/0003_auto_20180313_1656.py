# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-13 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_visits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
