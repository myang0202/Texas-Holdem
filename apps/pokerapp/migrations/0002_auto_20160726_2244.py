# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 22:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokerapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='pot',
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.IntegerField(),
        ),
    ]
