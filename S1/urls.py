from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^add$', views.auth_register),
    # url(r'^show$', views.represent_student_list),
    # url(r'^edit$', views.edit_student_info),
    # url(r'^remove$', views.remove_student),
]
