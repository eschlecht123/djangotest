# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer_multiplechoice_question', '0009_auto_20161116_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(default=b'multiplechoice', max_length=200),
        ),
    ]
