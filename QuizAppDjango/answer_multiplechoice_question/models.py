
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text1 = models.CharField(max_length=200, default='')
    answer_text2 = models.CharField(max_length=200, default='')
    answer_text3 = models.CharField(max_length=200, default='')
    answer_text4 = models.CharField(max_length=200, default='')

    correct_answer_1 = models.BooleanField()
    correct_answer_2 = models.BooleanField()
    correct_answer_3 = models.BooleanField()
    correct_answer_4 = models.BooleanField()

    question_type = models.CharField(max_length=200, default='multiplechoice')
    quiz = models.CharField(max_length=200, default='')


def __str__(self):
    return self.question_text