# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer_singlechoice_question', '0007_auto_20161110_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_text1',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_text2',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_text3',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_text4',
            field=models.CharField(default='', max_length=200),
        ),
    ]
