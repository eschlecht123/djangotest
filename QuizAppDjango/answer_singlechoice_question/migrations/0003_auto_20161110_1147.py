# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer_singlechoice_question', '0002_auto_20161109_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='option_1',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='option_2',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='option_3',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='option_4',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='true',
            field=models.CharField(max_length=2),
        ),
    ]
