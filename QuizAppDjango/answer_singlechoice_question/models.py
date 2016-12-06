
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text1 = models.CharField(max_length=200, default='')
    answer_text2 = models.CharField(max_length=200, default='')
    answer_text3 = models.CharField(max_length=200, default='')
    answer_text4 = models.CharField(max_length=200, default='')

    correct_answer = models.CharField(max_length=200)


def __str__(self):
    return self.question_text