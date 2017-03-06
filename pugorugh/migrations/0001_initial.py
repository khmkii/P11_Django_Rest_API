# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-27 13:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('image_path', models.ImageField(blank=True, null=True, upload_to='dogs/')),
                ('breed', models.CharField(max_length=155, null=True)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('f', 'Girl'), ('m', 'Boy'), ('u', 'Unknown Gender')], max_length=1)),
                ('size', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('l', 'Liked'), ('d', 'Disliked')], max_length=1)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(choices=[('b', 'Baby'), ('y', 'Young'), ('a', 'Adult'), ('s', 'Senior')], default=('b', 'y', 'a', 's'), max_length=8)),
                ('gender', models.CharField(choices=[('f', 'Girl'), ('m', 'Boy'), ('u', 'Unknown Gender')], default=('f', 'm', 'u'), max_length=4)),
                ('size', models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown Size')], default=('s', 'm', 'l', 'xl', 'u'), max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userdog',
            unique_together=set([('user', 'dog')]),
        ),
    ]
