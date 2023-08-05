# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-24 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('case_studies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file_ptr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='case_studies_image_related', serialize=False, to='files.File'),
        ),
    ]
