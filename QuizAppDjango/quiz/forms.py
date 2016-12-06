from django import forms
from .models import Course, Quiz, SingleChoiceQuestion, EssayQuestion, MultipleChoiceQuestion, TFQuestion


class CourseForm(forms.ModelForm):
    course_title = forms.CharField(max_length=50, widget = forms.TextInput(
           attrs = { 'placeholder': 'Kursname eingeben'}))
    semester = forms.IntegerField(widget = forms.TextInput(
           attrs = { 'placeholder': 'Semesterzahl eingeben'}))
    dozent = forms.CharField(max_length=50, widget = forms.TextInput(
           attrs = { 'placeholder': 'Name des Dozenten eingeben'}))

    class Meta:
        model = Course
        fields = '__all__'


class QuizForm(forms.ModelForm):
    quiz_title = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'Quiz Name einfuegen'}))

    class Meta:
        model = Quiz
        fields = '__all__'


class EssayQuestionForm(forms.ModelForm):
    essay_question_text = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'Frage eingeben'}))
    answer_text = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'Antwort eingeben'}))
    foreign_key_quiz_id = forms.HiddenInput()

    class Meta:
        model = EssayQuestion
        fields = ['essay_question_text','answer_text']


class SingleChoiceQuestionForm(forms.ModelForm):
    single_question_text = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'Frage eingeben'}))
    right_answer = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'erste Antwort eingeben'}))

    false_answer1 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'zweite Antwort eingeben'}))
    false_answer2 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'dritte Antwort eingeben'}))
    false_answer3 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'vierte Antwort eingeben'}))
    correct_answer1 = forms.CharField(max_length=1)

    class Meta:
        model = SingleChoiceQuestion
        fields = '__all__'


class MultipleChoiceQuestionForm(forms.ModelForm):
    multi_question_text = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'Frage eingeben'}))
    answer_text1 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'erste Antwort eingeben'}))
    answer_text2 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'zweite Antwort eingeben'}))
    answer_text3 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'dritte Antwort eingeben'}))
    answer_text4 = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'vierte Antwort eingeben'}))


    class Meta:
        model = MultipleChoiceQuestion
        fields = ['multi_question_text','answer_text1','answer_text2','answer_text3','answer_text4']


class TFQuestionForm(forms.ModelForm):
    tf_question_text = forms.CharField(max_length=200, widget = forms.TextInput(
           attrs = { 'placeholder': 'Frage eingeben'}))

    class Meta:
        model = TFQuestion
        fields = ['tf_question_text']
