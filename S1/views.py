from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, PackageLoader, select_autoescape
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
# Create your views here.

env = Environment(loader=PackageLoader('S1', 'Web/templates'))
env.globals.update({'static': staticfiles_storage.url("S1/"), 'url': reverse})


def index(request):
    template = env.get_template('container.html')
    return HttpResponse(template.render({
                            'addForm': env.get_template("add.html").render(),
                            'removeForm': env.get_template("remove.html").render(),
                            'editForm': env.get_template("edit.html").render(),
                        }))



def listStudents(request):
    template = env.get_template('list.html')
    list_content = template.render(data={'header': ['نام', 'نام خانوادگی', 'تاریخ تولد', 'کد ملی'],
                                         'body': [['آرمین', 'بهنام نیا', '16/8/1374', '0018569773'],
                                                  ['آرش', 'پوردامغانی', '16/8/1374', '0010010017'],
                                                  ['محسن', 'رحیمی', '16/8/1374', '0018569773']]
                                         }, request=request)
    return HttpResponse(list_content)
