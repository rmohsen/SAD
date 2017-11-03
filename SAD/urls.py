"""SAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from S1 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/add/?$', views.auth_register),
    url(r'^test/show/?$', views.represent_student_list),
    url(r'^test/edit/?$', views.edit_student_info),
    url(r'^test/remove/?$', views.remove_student),
    url(r'^test/', include('S1.urls'))
]
