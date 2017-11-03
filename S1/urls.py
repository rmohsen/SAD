from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getList$', views.listStudents, name="list_students"),
]
