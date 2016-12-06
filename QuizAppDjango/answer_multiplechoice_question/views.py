
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .forms import QuestionForm
from .models import Question
from django.http import HttpResponseRedirect
from django.views import generic
from random import randint
import random
from django.http import HttpResponse
import os, sys, sqlite3


class Index(generic.ListView):
    template_name = 'answer_multiplechoice_question/index.html'
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
        return HttpResponseRedirect('/answer_multiplechoice_question/')
    else:
        form = QuestionForm()
    return render_to_response('answer_multiplechoice_question/add_question.html', {'form': form}, context)


def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render_to_response('answer_multiplechoice_question/answer.html',
                              {'question': question, 'question_id': question_id})


def verify(request, question_id):
    # return HttpResponse("<h1>hallo<h1>")
    # k = Question.objects.get(id=question_id).correct_answer_1
    # p = request.GET.get('checks1')
    # return HttpResponse(p)
    global r
    if not request.GET.get('checks1') is None:
        checking1 = "True"
    else:
        checking1 = "False"

    if not request.GET.get('checks2') is None:
        checking2 = "True"
    else:
        checking2 = "False"

    if not request.GET.get('checks3') is None:
        checking3 = "True"
    else:
        checking3 = "False"

    if not request.GET.get('checks4') is None:
        checking4 = "True"
    else:
        checking4 = "False"

    # return HttpResponse(str(Question.objects.get(id=question_id).correct_answer_1))


    if str(Question.objects.get(id=question_id).correct_answer_1) == checking1:
        if str(Question.objects.get(id=question_id).correct_answer_2) == checking2:
            if str(Question.objects.get(id=question_id).correct_answer_3) == checking3:
                if str(Question.objects.get(id=question_id).correct_answer_4) == checking4:
                    return HttpResponse("hallo")



                    myList = []

                    connection = sqlite3.connect("db.sqlite3")
                    cursor = connection.cursor()

                    cursor.execute("""SELECT max(id) FROM answer_multiplechoice_question_question""")
                    max_id = cursor.fetchone()[0]

                    # return HttpResponse(max_id)


                    for i in range(1, max_id+1):

                        if Question.objects.get(id=i).quiz == 'tolles_quiz':
                            myList.append(Question.objects.get(id=i))


                    # max_id = cursor.fetchone()[0]

                    # return HttpResponse(myList)


                    return HttpResponse(myList)

                    while True:

                        r = str(randint(1, max_id))
                        if r != question_id: break
                    summary = r
                    # if Question.objects.all().count() < summary:
                    # return HttpResponseRedirect('/answer_multiplechoice_question/')
                    # print(request.POST.get('answer'),"eingetippt im if")
                    # print(Question.objects.get(id=question_id).answer_text, "gewollt im if")
                    return HttpResponseRedirect('/answer_multiplechoice_question/answer/%s' % summary)

                else:
                    # print("bin nirgends")
                    # print(request.POST.get('answer'), "eingetippt im else")
                    # print(Question.objects.get(id=question_id).answer_text, "gewollt im else")
                    return HttpResponseRedirect('/answer_multiplechoice_question/answer/%s' % question_id)

            else:
                # print("bin nirgends")
                # print(request.POST.get('answer'), "eingetippt im else")
                # print(Question.objects.get(id=question_id).answer_text, "gewollt im else")
                return HttpResponseRedirect('/answer_multiplechoice_question/answer/%s' % question_id)
        else:
            # print("bin nirgends")
            # print(request.POST.get('answer'), "eingetippt im else")
            # print(Question.objects.get(id=question_id).answer_text, "gewollt im else")
            return HttpResponseRedirect('/answer_multiplechoice_question/answer/%s' % question_id)
    else:
        # print("bin nirgends")
        # print(request.POST.get('answer'), "eingetippt im else")
        # print(Question.objects.get(id=question_id).answer_text, "gewollt im else")
        return HttpResponseRedirect('/answer_multiplechoice_question/answer/%s' % question_id)
