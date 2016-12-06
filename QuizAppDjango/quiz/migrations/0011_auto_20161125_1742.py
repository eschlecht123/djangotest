# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-25 16:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20161125_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='essayquestion',
            old_name='question_text',
            new_name='essay_question_text',
        ),
        migrations.RenameField(
            model_name='multiplechoicequestion',
            old_name='question_text',
            new_name='multi_question_text',
        ),
        migrations.RenameField(
            model_name='singlechoicequestion',
            old_name='question_text',
            new_name='single_question_text',
        ),
        migrations.RenameField(
            model_name='tfquestion',
            old_name='question_text',
            new_name='tf_question_text',
        ),
    ]
