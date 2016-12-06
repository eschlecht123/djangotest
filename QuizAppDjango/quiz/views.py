from __future__ import division
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.shortcuts import render_to_response
from .forms import CourseForm, QuizForm, EssayQuestionForm, SingleChoiceQuestionForm, MultipleChoiceQuestionForm, TFQuestionForm
from .models import Course, Quiz, EssayQuestion, SingleChoiceQuestion, MultipleChoiceQuestion, TFQuestion, Ergebnis
from django.http import HttpResponseRedirect
from datetime import datetime
from time import sleep
import time

from django.views import generic
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
import os, sys, sqlite3
import json
from itertools import cycle
from django.template.loader import render_to_string
from django.template import loader, Context
import random
import ctypes
#import Tkinter
#import tkMessageBox

array_index = 0
myList = []
anzahl = 0
max_id_multiplechoice = 0
max_id_singlechoice = 0
max_id_truefalse = 0
max_id_essay = 0
starttime = None
endtime = None
gesamtpunktzahl = 0

def index(request):
    return render(request, 'quiz/index.html')


def settings(request):
    return render_to_response('quiz/settings.html')


def add_course(request):
    context = RequestContext(request)
    if request.method == 'POST':

        form = CourseForm(request.POST)
        if form.is_valid():
            course_title = request.POST.get('course_title')
            semester = request.POST.get('semester')
            dozent = request.POST.get('dozent')
            c_obj = Course(course_title=course_title,
                           semester=semester,
                           dozent=dozent)
            c_obj.save()
        return HttpResponseRedirect('/quiz/settings/')
    else:
        form = CourseForm()
    return render_to_response('quiz/add_course.html', {'form': form}, context)


def add_course_rename(request, course_id):
    context = RequestContext(request)
    if request.method == 'POST':

        form = CourseForm(request.POST)
        if form.is_valid():
            c_obj = get_object_or_404(Course, pk=course_id)
            c_obj.course_title = request.POST.get('course_title')
            c_obj.semester = request.POST.get('semester')
            c_obj.dozent = request.POST.get('dozent')
            c_obj.id = course_id
            c_obj.save()
        return HttpResponseRedirect('/quiz/update_course/')
    else:
        form = CourseForm()
    return render_to_response('quiz/add_course.html', {'form': form}, context)


def add_quiz(request):
    context = RequestContext(request)
    if request.method == 'POST':

        form = QuizForm(request.POST)
        if form.is_valid():
            quiz_title = request.POST.get('quiz_title')
            coursefk_id = request.POST.get('coursefk')
            q_obj = Quiz(quiz_title=quiz_title,
                         coursefk_id=coursefk_id)
            q_obj.save()
        return HttpResponseRedirect('/quiz/%s/add_question/' % q_obj.id)
    else:
        form = QuizForm()
    return render_to_response('quiz/add_quiz.html', {'form': form}, context)


def add_quiz_rename(request, quiz_id):
    context = RequestContext(request)
    if request.method == 'POST':

        form = QuizForm(request.POST)
        if form.is_valid():
            q_obj = get_object_or_404(Quiz, pk=quiz_id)
            q_obj.quiz_title = request.POST.get('quiz_title')
            q_obj.coursefk_id = request.POST.get('coursefk')
            q_obj.id = quiz_id
            q_obj.save()
        return HttpResponseRedirect('/quiz/update_quiz/')
    else:
        form = QuizForm()
    return render_to_response('quiz/add_quiz.html', {'form': form}, context)


def add_question(request, quiz_id):
    context = RequestContext(request)
    if request.POST.get('essay') == 'Begriffs Frage':
        form = EssayQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage"}, context)

    if request.POST.get('single') == 'single':
        form = SingleChoiceQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Single Choice Question"}, context)

    if request.POST.get('multi') == 'MultipleChoice Frage':
        form = MultipleChoiceQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Multiple Choice Frage", 'a':True}, context)

    if request.POST.get('truefalse') == 'WahrFalsch Frage':
        form = TFQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Wahr/Falsch Frage",'b':True}, context)

    if request.POST.get('essay_question_text'):
        form = EssayQuestionForm(request.POST)
        if form.is_valid():
            q_obj = EssayQuestion(essay_question_text=request.POST.get('essay_question_text'),
                                  answer_text=request.POST.get('answer_text').lower(),
                                  quizfk_id=quiz_id)
            q_obj.save()
            form = EssayQuestionForm()
        return render_to_response('quiz/addquestionselect.html', {'form': form, 'quiz_id': quiz_id,'Question': "Begriffs Frage"}, context)

    if request.POST.get('single_question_text'):
        form = SingleChoiceQuestionForm(request.POST)
        if form.is_valid():
            scq_obj = SingleChoiceQuestion(single_question_text=request.POST.get('single_question_text'),
                                           false_answer1=request.POST.get('false_answer1'),
                                           false_answer2=request.POST.get('false_answer2'),
                                           false_answer3=request.POST.get('false_answer3'),
                                           right_answer=request.POST.get('right_answer'),
                                           quizfk_id=quiz_id)
            scq_obj.save()
        return render_to_response('quiz/addquestionselect.html', {'form': form, 'quiz_id': quiz_id}, context)

    if request.POST.get('tf_question_text'):
        form = TFQuestionForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('drop')) == "True":
                true_or_false = True
            else:
                true_or_false = False

            mq_obj = TFQuestion(tf_question_text=request.POST.get('tf_question_text'),
                                true_or_false=true_or_false,
                                question_type="truefalse",
                                quizfk_id=quiz_id)
            mq_obj.save()
            form = TFQuestionForm()
        return render_to_response('quiz/addquestionselect.html',{'form': form, 'quiz_id': quiz_id, 'Question': "True or False Question", 'b': True},
                              context)

    if request.POST.get('multi_question_text'):
        form = MultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('drop')) == "1":
                correct_answer_1 = True

            else:
                correct_answer_1 = False
            if str(request.POST.get('drop')) == "2":
                correct_answer_2 = True
            else:
                correct_answer_2 = False
            if str(request.POST.get('drop')) == "3":
                correct_answer_3 = True
            else:
                correct_answer_3 = False
            if str(request.POST.get('drop')) == "4":
                correct_answer_4 = True
            else:
                correct_answer_4 = False

            mq_obj = MultipleChoiceQuestion(multi_question_text=request.POST.get('multi_question_text'),
                                            answer_text1=request.POST.get('answer_text1'),
                                            answer_text2=request.POST.get('answer_text2'),
                                            answer_text3=request.POST.get('answer_text3'),
                                            answer_text4=request.POST.get('answer_text4'),
                                            correct_answer_1=correct_answer_1,
                                            correct_answer_2=correct_answer_2,
                                            correct_answer_3=correct_answer_3,
                                            correct_answer_4=correct_answer_4,
                                            quizfk_id=quiz_id)
            mq_obj.save()
            form = MultipleChoiceQuestionForm()
            return render_to_response('quiz/addquestionselect.html',
                                      {'form': form, 'quiz_id': quiz_id, 'Question': "Multiple Choice Question",
                                       'a': True},
                                      context)

    else:
        form = EssayQuestionForm()
    return render_to_response('quiz/addquestionselect.html',
                              {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage"}, context)

    if request.POST.get('fertig'):
        return render(request, 'quiz/add_quiz.html', context)


def fill_quiz(request):
    all_quiz = Quiz.objects.all()
    context = {
        'all_quiz': all_quiz
    }
    return render(request, 'quiz/fill_quiz.html', context)


def choose(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    all_question = EssayQuestion.objects.all()

    return render_to_response('quiz/choose.html', {'quiz': quiz, 'quiz_id': quiz_id, 'all_question': all_question})


def course_select(request):
    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_course = Course.objects.filter(course_title__startswith=search_query)
        if all_course.count() != 0:
            return render(request, 'quiz/course_select.html', {'all_course': all_course}, context)
        else:
            print('Suche ohne Treffer :(')
    else:
        all_course = Course.objects.all()
        print(all_course)
    return render(request, 'quiz/course_select.html', {'all_course': all_course}, context)


def quiz_select(request, course_id):
    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_quiz = Quiz.objects.filter(coursefk_id=course_id, quiz_title__startswith=search_query)
        if all_quiz.count() != 0:
            return render(request, 'quiz/quiz_select.html', {'all_quiz': all_quiz}, context)
        else:
            print('Suche ohne Treffer :(')
    else:
        all_quiz = Quiz.objects.filter(coursefk_id=course_id)
        print(all_quiz)
    return render(request, 'quiz/quiz_select.html', {'all_quiz': all_quiz}, context)


def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    print('Quiz mit ID', quiz_id, 'deleted.')

    return HttpResponseRedirect('/quiz/update_quiz/')


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    print('Kurs mit ID', course_id, 'deleted.')

    return HttpResponseRedirect('/quiz/update_course/')

def delete_tfquestion(request, TFQuestion_id):
    tquestion = get_object_or_404(TFQuestion, id=TFQuestion_id)
    tquestion.delete()
    return HttpResponseRedirect('/quiz/update_question/')
def delete_essayquestion(request, EssayQuestion_id):
    equestion = get_object_or_404(EssayQuestion, id=EssayQuestion_id)
    equestion.delete()
    return HttpResponseRedirect('/quiz/update_question/')
def delete_singlechoicequestion(request, SingleChoiceQuestion_id):
    squestion = get_object_or_404(SingleChoiceQuestion, id=SingleChoiceQuestion_id)
    squestion.delete()
    return HttpResponseRedirect('/quiz/update_question/')
def delete_multiplechoicequestion(request, MultipleChoiceQuestion_id):
    mquestion = get_object_or_404(MultipleChoiceQuestion, id=MultipleChoiceQuestion_id)
    mquestion.delete()
    return HttpResponseRedirect('/quiz/update_question/')


def update_quiz(request):
    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_quiz = Quiz.objects.filter(quiz_title__startswith=search_query)
        if all_quiz.count() != 0:
            return render(request, 'quiz/update_quiz.html', {'all_quiz': all_quiz}, context)
        else:
            print('Suche ohne Treffer :(')
    else:
        all_quiz = Quiz.objects.all()
    return render(request, 'quiz/update_quiz.html', {'all_quiz': all_quiz}, context)


def update_course(request):
    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_course = Course.objects.filter(course_title__startswith=search_query)
        print(all_course)
        if all_course.count() != 0:
            return render(request, 'quiz/update_course.html', {'all_course': all_course}, context)
        else:
            print('Suche ohne Treffer :(')
    else:
        all_course = Course.objects.all()
    return render(request, 'quiz/update_course.html', {'all_course': all_course}, context)

def update_question(request):
    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        tquestion = TFQuestion.objects.filter(tf_question_text__startswith=search_query)
        equestion = EssayQuestion.objects.filter(essay_question_text__startswith=search_query)
        squestion = SingleChoiceQuestion.objects.filter(single_question_text__startswith=search_query)
        mquestion = MultipleChoiceQuestion.objects.filter(multi_question_text__startswith=search_query)
        return render(request, 'quiz/update_question.html', {'tquestion': tquestion,
                                                     'equestion': equestion,
                                                     'sequestion': squestion,
                                                     'mquestion': mquestion}, context)
    else:
        tquestion = TFQuestion.objects.all()
        equestion = EssayQuestion.objects.all()
        squestion = SingleChoiceQuestion.objects.all()
        mquestion = MultipleChoiceQuestion.objects.all()
    return render(request, 'quiz/update_question.html', {'tquestion': tquestion,
                                                     'equestion': equestion,
                                                     'sequestion': squestion,
                                                     'mquestion': mquestion}, context)



def answer_quiz(request, quiz_id):











    #return HttpResponse(1)
    quiz = get_object_or_404(Quiz, pk=quiz_id)


    global myList
    if len(myList)==0:
        print("Array leer")

        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()

        global max_id_essay
        global max_id_truefalse
        global max_id_multiplechoice
        global max_id_singlechoice
        if str(len(MultipleChoiceQuestion.objects.all()))!=0:
            cursor.execute("""SELECT max(id) FROM quiz_multiplechoicequestion""")
            max_id_multiplechoice = cursor.fetchone()[0]
        else:max_id_multiplechoice=0
        if str(len(SingleChoiceQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_singlechoicequestion""")
            max_id_singlechoice = cursor.fetchone()[0]
        else: max_id_singlechoice = 0
        if str(len(TFQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_tfquestion""")
            max_id_truefalse = cursor.fetchone()[0]
        else:max_id_truefalse = 0
        if str(len(EssayQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_essayquestion""")
            max_id_essay = cursor.fetchone()[0]
        else: max_id_essay = int(0)
        print("kein Essay")

        #return HttpResponse(max_id_essay)

        global anzahl
        global max_id_multiplechoice
        global max_id_singlechoice
        global max_id_truefalse
        global max_id_essay
        anzahl = 0

        if str(len(MultipleChoiceQuestion.objects.all())) != 0:
            if max_id_multiplechoice is not None:
                for i in (MultipleChoiceQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)
                        anzahl= anzahl + 1

        if str(len(SingleChoiceQuestion.objects.all())) != 0:
            if max_id_singlechoice is not None:
                for i in (SingleChoiceQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)
                        anzahl = anzahl +1
        if str(len(TFQuestion.objects.all())) != 0:
            if max_id_truefalse is not None:
                for i in (TFQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)#
                        anzahl = anzahl +1
        if str(len(EssayQuestion.objects.all())) != 0:
            if max_id_essay is not None:
                for i in (EssayQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:

                        myList.append(i)
                        anzahl = anzahl +1

        random.shuffle(myList)


    #return HttpResponse(question)

    #return render_to_response('quiz/answer_multiplechoice.html', {'question': question, 'question_id': question_id})




    #return render(request, 'quiz/answer_multiplechoice.html', {'question': question})

    #url = '/quiz/' + quiz_id + '/answer_quiz/0'
    #return HttpResponseRedirect(url)

    if len(myList) != 0:
        global anzahl
        global max_id_multiplechoice
        global max_id_singlechoice
        global max_id_truefalse
        global max_id_essay
        global array_index



        if str(myList[0].quizfk.id) != str(quiz_id):
            myList = []
            array_index = 0
            anzahl = 0
            print("Andere quiz_id")

            global myList
            myList = []
            connection = sqlite3.connect("db.sqlite3")
            cursor = connection.cursor()

            cursor.execute("""SELECT max(id) FROM quiz_multiplechoicequestion""")
            max_id_multiplechoice = cursor.fetchone()[0]
            cursor.execute("""SELECT max(id) FROM quiz_singlechoicequestion""")
            max_id_singlechoice = cursor.fetchone()[0]
            cursor.execute("""SELECT max(id) FROM quiz_tfquestion""")
            max_id_truefalse = cursor.fetchone()[0]
            cursor.execute("""SELECT max(id) FROM quiz_essayquestion""")
            max_id_essay = cursor.fetchone()[0]

            # return HttpResponse(max_id_essay)



            if max_id_multiplechoice is None:
                max_id_multiplechoice = 0

            if max_id_singlechoice is None:
                max_id_singlechoice = 0

            if max_id_truefalse is None:
                max_id_truefalse = 0

            if max_id_essay is None:
                max_id_essay = 0




            for i in (MultipleChoiceQuestion.objects.all()):


                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)
                    anzahl = anzahl + 1

            for i in (SingleChoiceQuestion.objects.all()):


                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)
                    anzahl = anzahl + 1

            for i in (TFQuestion.objects.all()):

                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)  #
                    anzahl = anzahl + 1

            for i in (EssayQuestion.objects.all()):


                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)
                    anzahl = anzahl + 1

                random.shuffle(myList)

    if request.GET.get('Weiter') == 'Weiter':
        if array_index == anzahl - 1:
            global array_index
            global anzahl
            global myList
            array_index = 0
            anzahl = 0
            myList = []
            print("gesamtpunktzahl" + str(gesamtpunktzahl))


            erg_obj = Ergebnis(quiz=quiz, punkte=gesamtpunktzahl)
            erg_obj.save()
            return render_to_response('quiz/finish.html',{'gesamtpunktzahl': gesamtpunktzahl, 'quiz': quiz})
        else:
            array_index = array_index + 1

            # return HttpResponse(array_index)

            question = myList[array_index]
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
            global starttime
            global endtime

            starttime = datetime.now()

            if question.question_type == 'multiplechoice':
                return render_to_response('quiz/answer_multiplechoice.html',{'question': question, 'stand': stand, 'prozent': prozent})
            elif question.question_type == 'singlechoice':
                return render_to_response('quiz/answer_singlechoice.html',{'question': question, 'stand': stand, 'prozent': prozent})
            elif question.question_type == 'truefalse':
                return render_to_response('quiz/answer_truefalse.html',{'question': question, 'stand': stand, 'prozent': prozent})
            elif question.question_type == 'essay':
                return render_to_response('quiz/answer_essay.html',{'question': question, 'stand': stand, 'prozent': prozent})

            return HttpResponseRedirect('/quiz/')




    elif request.GET.get('Fertig') == 'true':

        question = myList[array_index]
        if str(myList[array_index].true_or_false) == 'True':

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html', {'question': question, 'r': True})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html', {'question': question, 'f': True})

    elif request.GET.get('Fertig') == 'wahr':


        question = myList[array_index]
        prozent = ((array_index + 1) / anzahl) * 100
        print(array_index + 1)
        print(anzahl)
        p = 1 / anzahl
        round(prozent, 3)
        print("p" + str(prozent))
        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
        if str(myList[array_index].true_or_false) == 'True':
            global starttime
            global endtime
            endtime = datetime.now()
            timedelta = endtime - starttime
            print("timedelta" + str(timedelta.seconds))
            punktzahl = 10 - int(timedelta.seconds)
            if punktzahl < 1:
                punktzahl = 1
            global gesamtpunktzahl
            gesamtpunktzahl = gesamtpunktzahl + punktzahl

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html', {'question': question, 'r': True, 'stand': stand, 'prozent':prozent, 'punktzahl': punktzahl})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html', {'question': question, 'f': True, 'stand': stand, 'prozent':prozent})






    elif request.GET.get('Fertig') == 'falsch':


        question = myList[array_index]
        prozent = ((array_index + 1) / anzahl) * 100
        p = 1 / anzahl
        round(prozent, 3)
        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
        if str(myList[array_index].true_or_false) == 'False':
            global starttime
            global endtime
            endtime = datetime.now()
            timedelta = endtime - starttime
            punktzahl = 10 - int(timedelta.seconds)
            if punktzahl < 1:
                punktzahl = 1
            global gesamtpunktzahl
            gesamtpunktzahl = gesamtpunktzahl + punktzahl

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html',{'question': question, 'r': True, 'stand': stand, 'prozent':prozent, 'punktzahl': punktzahl})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html', {'question': question, 'f': True, 'stand': stand, 'prozent':prozent})


    elif request.GET.get('Fertig') == 'Fertig':
        global starttime
        global endtime
        endtime = datetime.now()
        timedelta = endtime - starttime

















        if myList[array_index].question_type == 'multiplechoice':


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
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)


            if str(myList[array_index].correct_answer_1) == checking1:
                if str(myList[array_index].correct_answer_2) == checking2:
                    if str(myList[array_index].correct_answer_3) == checking3:
                        if str(myList[array_index].correct_answer_4) == checking4:
                            global starttime
                            global endtime
                            endtime = datetime.now()
                            timedelta = endtime - starttime
                            punktzahl = 10 - int(timedelta.seconds)
                            if punktzahl < 1:
                                punktzahl = 1
                            global gesamtpunktzahl
                            gesamtpunktzahl = gesamtpunktzahl + punktzahl

                            question = myList[array_index]

                            antwort_ist = 'Richtig'
                            return render_to_response('quiz/answer_multiplechoice.html',
                                                      {'question': question, 'r': True})
                        #else:
                         #   antwort_ist = 'Falsch'
                          ##  return render_to_response('quiz/answer_multiplechoice.html',
                            #                          {'question': question, 'f': True})









                            print('user clicked summary')

                        else:
                            question = myList[array_index]
                            return render_to_response('quiz/answer_multiplechoice.html',
                                                      {'question': question, 'f': True})
                    else:
                        question = myList[array_index]
                        return render_to_response('quiz/answer_multiplechoice.html',
                                                  {'question': question, 'f': True})
                else:
                    question = myList[array_index]
                    return render_to_response('quiz/answer_multiplechoice.html',
                                              {'question': question, 'f': True})
            else:
                question = myList[array_index]
                return render_to_response('quiz/answer_multiplechoice.html',
                                          {'question': question, 'f': True})










        elif myList[array_index].question_type == 'singlechoice':

            #return HttpResponse(array_index)
            question = myList[array_index]
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
            if myList[array_index].correct_answer == request.GET.get('checks'):
                global starttime
                global endtime
                endtime = datetime.now()
                timedelta = endtime - starttime
                punktzahl = 10 - int(timedelta.seconds)
                if punktzahl < 1:
                    punktzahl = 1
                global gesamtpunktzahl
                gesamtpunktzahl = gesamtpunktzahl + punktzahl
                antwort_ist = 'Richtig'
                return render_to_response('quiz/answer_singlechoice.html',{'question': question, 'r': True, 'stand': stand, 'prozent':prozent, 'punktzahl': punktzahl})
            else:
                antwort_ist = 'Falsch'
                return render_to_response('quiz/answer_singlechoice.html',{'question': question, 'f': True, 'stand': stand, 'prozent':prozent})





        elif myList[array_index].question_type == 'essay':

            question = myList[array_index]
            #return HttpResponse(array_index)
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
            if myList[array_index].answer_text.lower() == request.GET.get('answer').lower():
                global starttime
                global endtime
                endtime = datetime.now()
                timedelta = endtime - starttime
                punktzahl = 10 - int(timedelta.seconds)
                if punktzahl < 1:
                    punktzahl = 1
                global gesamtpunktzahl
                gesamtpunktzahl = gesamtpunktzahl + punktzahl
                antwort_ist = 'Richtig'
                return render_to_response('quiz/answer_essay.html',
                                          {'question': question, 'r': True, 'stand': stand, 'prozent':prozent, 'punktzahl': punktzahl})
            else:
                antwort_ist = 'Falsch'
                return render_to_response('quiz/answer_essay.html',
                                          {'question': question, 'f': True, 'stand': stand, 'prozent':prozent})



    global myList
    if len(myList)==0:
        search_query = ''
        message = 'Quiz leer'
        all_quiz = Quiz.objects.filter(quiz_title__startswith=search_query)

        #return HttpResponseRedirect('/quiz/quiz_select/')
        return render(request, 'quiz/quiz_select.html', {'all_quiz': all_quiz, 'message': message, 'e': True})


    else:

        global starttime
        global endtime
        global gesamtpunktzahl
        gesamtpunktzahl = 0

        starttime = datetime.now()











        global array_index
        array_index = 0
        question = myList[array_index]
        prozent = ((array_index+1)/anzahl)*100

        p = 1/anzahl
        round(prozent, 3)

        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)


    global myList
    if len(myList)==0:
        message = 'Quiz leer'

        #return HttpResponseRedirect('/quiz/quiz_select/')
        return render_to_response('quiz/quiz_empty.html', {'message': message})

    else:
        
        antwort_ist = 'Viel Spass'
        global array_index
        array_index = 0
        question = myList[array_index]
        print(antwort_ist)
        if question.question_type == 'multiplechoice':
            return render_to_response('quiz/answer_multiplechoice.html',{'question': question, 'stand': stand, 'prozent':prozent})
        elif question.question_type == 'singlechoice':
            return render_to_response('quiz/answer_singlechoice.html',{'question': question, 'stand': stand, 'prozent':prozent})
        elif question.question_type == 'truefalse':
            return render_to_response('quiz/answer_truefalse.html',{'question': question, 'stand': stand, 'prozent':prozent})
        elif question.question_type == 'essay':
            return render_to_response('quiz/answer_essay.html',{'question': question, 'stand': stand, 'prozent':prozent})

