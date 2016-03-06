from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /sportsman/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^thisurlshouldbechanged123/$', views.StudentEvaluationListView.as_view(), name='studentEvaluations'),
    url(r'^thisurlshouldbechanged123/certificate/$', views.gen_certificates, name='studentEvaluationCertificate'),
    url(r'^studentEvaluations/(?P<student_evaluation_id>[0-9]+)/certificate/$', views.gen_certificate, name='studentEvaluationCertificate'),
]
