# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-05 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0003_auto_20170305_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown Size')], max_length=2),
        ),
    ]
