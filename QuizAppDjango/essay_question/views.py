from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .forms import QuestionForm
from models import Question
from django.http import HttpResponseRedirect
from django.views import generic


class Index(generic.ListView):
    template_name = 'essay_question/index.html'
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
        return HttpResponseRedirect('/essay_question/')
    else:
        form = QuestionForm()
    return render_to_response('essay_question/add_equestion.html', {'form': form}, context)


def answer(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render_to_response('essay_question/answer.html', {'question': question, 'question_id': question_id})


def verify(request, question_id):
    if Question.objects.get(id=question_id).answer_text == request.POST.get('answer').lower():
        summary = int(question_id) + int(1)
        # if Question.objects.all().count() < summary:
           # return HttpResponseRedirect('/essay_question/')
        # print(request.POST.get('answer'),"eingetippt im if")
        # print(Question.objects.get(id=question_id).answer_text, "gewollt im if")
        return HttpResponseRedirect('/essay_question/answer/%s' % summary)

    else:
        # print("bin nirgends")
        # print(request.POST.get('answer'), "eingetippt im else")
        # print(Question.objects.get(id=question_id).answer_text, "gewollt im else")
        return HttpResponseRedirect('/essay_question/answer/%s' % question_id)