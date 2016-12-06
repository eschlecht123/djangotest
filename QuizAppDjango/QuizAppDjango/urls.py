from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^answer_multiplechoice_question/', include('answer_multiplechoice_question.urls')),
    url(r'^answer_singlechoice_question/', include('answer_singlechoice_question.urls')),
    url(r'^answer_true_false_question/', include('answer_true_false_question.urls')),


]
