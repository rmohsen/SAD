from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, PackageLoader, select_autoescape
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
# Create your views here.

def index(request):
    env = Environment(loader=PackageLoader('S1', 'Web/templates'), autoescape=select_autoescape(['html', 'xml']))
    env.globals.update({'static': staticfiles_storage.url("S1/"), 'url': reverse})
    template = env.get_template('container.html')
    return HttpResponse(template.render(data={'header': ['نام', 'نام خانوادگی', 'تاریخ تولد', 'کد ملی'],
                                         'body': [['آرمین', 'بهنام نیا', '16/8/1374', '0018569773'],
                                                  ['آرش', 'پوردامغانی', '16/8/1374', '0010010017'],
                                                  ['محسن', 'رحیمی', '16/8/1374', '0018569773']]
                                         }))
