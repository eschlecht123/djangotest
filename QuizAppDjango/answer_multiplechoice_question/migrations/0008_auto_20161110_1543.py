# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer_multiplechoice_question', '0007_auto_20161110_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer_1',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer_2',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer_3',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer_4',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
