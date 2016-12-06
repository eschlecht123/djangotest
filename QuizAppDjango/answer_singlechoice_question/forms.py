from django import forms
from .models import Question


class QuestionForm (forms.ModelForm):
    question_text = forms.CharField(max_length=200, help_text="Insert Question")
    answer_text = forms.CharField(max_length=200, help_text="insert Answer")

    class Meta:
        model = Question
        fields = '__all__'

