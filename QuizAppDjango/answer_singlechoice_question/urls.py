from django.conf.urls import url
from . import views
from .views import Index


app_name = 'answer_singlechoice_question'

urlpatterns = [
    url(r'^$', Index.as_view(), name='Index'),
    url(r'^add_question/$', views.add_question, name='addquestion'),
    url(r'^answer/(?P<question_id>[0-9]+)/$', views.answer, name='answer'),
    url(r'^answer/(?P<question_id>[0-9]+)/verify/$',views.verify, name='verify'),
]