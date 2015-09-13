from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /sportsman/
    url(r'^$', views.index, name='index'),
]
