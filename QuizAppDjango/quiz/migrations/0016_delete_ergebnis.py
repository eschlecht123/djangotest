# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 14:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_ergebnis_punkte'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ergebnis',
        ),
    ]
