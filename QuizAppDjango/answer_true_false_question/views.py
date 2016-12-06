from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .forms import QuestionForm
from .models import Question
from django.http import HttpResponseRedirect
from django.views import generic
from random import randint
import random
import sqlite3

class Index(generic.ListView):
    template_name = 'answer_true_false_question/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-id')


def add_question(request):
    context = RequestContext(request)
    if request.method == 'POST':

        form = QuestionForm(request.POST)
        if form.is_valid():
            # question_text = request.POST.get('question_text')
            # answer_text = request.POST.get('answer_text')
            q_obj = Question(question_text=request.POST.get('question_text'),
                             answer_text=request.POST.get('answer_text'))
            q_obj.save()
        return HttpResponseRedirect('/answer_true_false_question/')
    else:
        form = QuestionForm()
    return render_to_response('answer_true_false_question/add_question.html', {'form': form}, context)


def answer(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render_to_response('answer_true_false_question/answer.html', {'question': question, 'question_id': question_id})


def verify(request, question_id):
    global r
    if Question.objects.get(id=question_id).true == request.POST.get('verify').lower():
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()

        cursor.execute("""SELECT max(id) FROM answer_true_false_question_question""")
        max_id = cursor.fetchone()[0]

        while True:

            r = str(randint(1, max_id))
            if r != question_id: break
        summary = r
        # if Question.objects.all().count() < summary:
           # return HttpResponseRedirect('/answer_true_false_question/')
        # print(request.POST.get('answer'),"eingetippt im if")
        # print(Question.objects.get(id=question_id).answer_text, "gewollt im if")
        return HttpResponseRedirect('/answer_true_false_question/answer/%s' % summary)

    else:
        # print("bin nirgends")
        # print(request.POST.get('answer'), "eingetippt im else")
        # print(Question.objects.get(id=question_id).answer_text, "gewollt im else")
        return HttpResponseRedirect('/answer_true_false_question/answer/%s' % question_id)
