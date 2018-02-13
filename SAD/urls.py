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
    url(r'^test/', views.get_main_page),
    url(r'^test_get_name/', views.get_name),

    url(r'^test_sign_in/', views.get_signin),
    url(r'^test_sign_in_acc/', views.get_signin_acc),
    url(r'^test_sign_in_modir/', views.get_signin_modir),

    url(r'^test_karbari/', views.get_student_karbari),
    url(r'^test_karbari_acc/', views.get_acc_karbari),
    url(r'^test_karbari_modir/', views.get_modir_karbari),

    url(r'^test_get_processes/', views.show_processes),
    url(r'^test_show_process/', views.show_process),
    url(r'^test_get_process/', views.get_process ),

    url(r'^test_show_cartable/', views.show_account_cartable),

    url(r'^test_add_process_type/', views.create_process_type),
    url(r'^test_get_transactions/', views.get_transactions),

    url(r'^tes_main/', views.show_main_page),
    url(r'^admin/', admin.site.urls),
    url(r'^test/add/?$', views.auth_register),
    url(r'^test/edit/?$', views.edit_student_info),
    url(r'^test/remove/?$', views.remove_student),
    url(r'^test/', include('S1.urls'))
]
# <a href="http://127.0.0.1:8000/test_add_process_type/" name="add_process_type">add process type</a>
# <a href="http://127.0.0.1:8000/test_get_transactions/