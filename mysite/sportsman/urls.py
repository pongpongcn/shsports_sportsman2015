from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet, base_name='Student')

urlpatterns = [
    # ex: /sportsman/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^thisurlshouldbechanged123/$', views.StudentEvaluationListView.as_view(), name='studentEvaluations'),
    url(r'^thisurlshouldbechanged123/certificate/$', views.gen_certificates, name='studentEvaluationCertificate'),
    url(r'^studentEvaluations/(?P<student_evaluation_id>[0-9]+)/certificate/$', views.gen_certificate, name='studentEvaluationCertificate'),
]
