from django.conf.urls import url
from . import views

app_name = 'quiz'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^add_quiz/$', views.add_quiz, name='add_quiz'),
    #update quiz mit der quiz_id
    url(r'^add_quiz/(?P<quiz_id>[0-9]+)/$', views.add_quiz_rename, name='add_quiz_rename'),
    url(r'^add_course/$', views.add_course, name='add_course'),
    url(r'^add_course/(?P<course_id>[0-9]+)/$', views.add_course_rename, name='add_course_rename'),
    url(r'^fill_quiz/$', views.fill_quiz, name='fill_quiz'),
    #url(r'^fill_quiz/(?P<quiz_id>[0-9]+)/$', views.choose, name='choose'),
    url(r'^(?P<quiz_id>[0-9]+)/add_question/$', views.add_question, name="addquestionselect"),
    url(r'^(?P<course_id>[0-9]+)/quiz_select/$', views.quiz_select, name='quiz_select'),
    url(r'^course_select/$', views.course_select, name='course_select'),
    url(r'^delete_quiz/(?P<quiz_id>[0-9]+)/$', views.delete_quiz, name='delete_quiz'),
    url(r'^delete_course/(?P<course_id>[0-9]+)/$', views.delete_course, name='delete_course'),
    url(r'^update_course/$', views.update_course, name='update_course'),
    url(r'^update_quiz/$', views.update_quiz, name='update_quiz'),
    url(r'^(?P<quiz_id>[0-9]+)/answer_quiz/$', views.answer_quiz, name="answer_quiz"),
    url(r'^(?P<quiz_id>[0-9]+)/answer_quiz/(?P<array_id>[0-9]+)/$', views.answer_quiz, name="answer_quiz"),
    #url(r'^(?P<quiz_id>[0-9]+)/answer_quiz/(?P<array_id>[0-9]+)/verify/$', views.verify_multiplechoice, name="verifyMulitplechoice"),
    url(r'^update_question/$', views.update_question, name='update_question'),
    url(r'^delete_tfquestion/(?P<TFQuestion_id>[0-9]+)/$', views.delete_tfquestion, name='delete_tfquestion'),
    url(r'^delete_essayquestion/(?P<EssayQuestion_id>[0-9]+)/$', views.delete_essayquestion, name='delete_essayquestion'),
    url(r'^delete_singlechoicequestion/(?P<SingleChoiceQuestion_id>[0-9]+)/$', views.delete_singlechoicequestion, name='delete_singlechoicequestion'),
    url(r'^delete_multiplechoicequestion/(?P<MultipleChoiceQuestion_id>[0-9]+)/$', views.delete_multiplechoicequestion, name='delete_multiplechoicequestion'),

]
