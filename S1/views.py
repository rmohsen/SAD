# from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, PackageLoader, select_autoescape
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

# Create your views here.
from S1.models import Student
from datetime import date


env = Environment(loader=PackageLoader('S1', 'Web/templates'))
env.globals.update({'static': staticfiles_storage.url("S1/"), 'url': reverse})


def index(request):
    template = env.get_template('container.html')
    return HttpResponse(template.render({
                            'addForm': env.get_template("add.html").render(),
                            'removeForm': env.get_template("remove.html").render(),
                            'editForm': env.get_template("edit.html").render(),
                        }))



# def listStudents(request):
#     template = env.get_template('list.html')
#     list_content = template.render(data={'header': ['نام', 'نام خانوادگی', 'تاریخ تولد', 'کد ملی'],
#                                          'body': [['آرمین', 'بهنام نیا', '16/8/1374', '0018569773'],
#                                                   ['آرش', 'پوردامغانی', '16/8/1374', '0010010017'],
#                                                   ['محسن', 'رحیمی', '16/8/1374', '0018569773']]
#                                          }, request=request)
#     return HttpResponse(list_content)


def date_parser(input_date):
    year = ""
    month = ""
    day = ""
    (year, month, day) = input_date.split('-')

    return date(year=int(year), month=int(month), day=int(day))


def auth_register(request):
    # post
    if request.method == 'POST':
        # try:
        t = request.POST
        if (t['national_id'] == '' or t['first_name'] == '' or t['last_name'] == '' or t['birth_date'] == ''):
            raise Http404("hame mawared")
        if Student.objects.filter(identity_code=t['national_id']).exists():
            raise Http404("user tekrari")
        print(t['birth_date'])
        student = Student.objects.create(identity_code=t.get('national_id'),
                                         first_name=t.get('first_name'),
                                         last_name=t.get('last_name'),
                                         birth_date=date_parser(t.get('birth_date'))
                                         )
        # user.last_name = t['last_name']
        # user.first_name = t['first_name']
        # user.save()
        #
        # student = Student(user=user, birth_date=date_parser(t['birth_date']))
        # student.save()
        # except:
        #     raise Http404("problem1!")
        return HttpResponse('successful sign up')


def represent_student_list(request):
    student_list = Student.objects.all()
    env = Environment(loader=PackageLoader('S1', 'Web/templates'))
    env.globals.update({'static': staticfiles_storage.url("S1/"), 'url': reverse})
    template = env.get_template('list.html')
    data = {'header': ['نام', 'نام خانوادگی', 'تاریخ تولد', 'شماره شناسنامه'],
            'body': [],
            }
    for s in student_list:
        list = data['body']
        list.append([s.first_name,s.last_name,s.birth_date,s.identity_code])
    list_content = template.render(data=data)
    return HttpResponse(list_content)

def edit_student_info(request):
    t = request.POST

    # user = User.objects.get(username=t['national_id'])
    try:
        student = Student.objects.get(identity_code=t.get('national_id'))
    except:
        raise Http404("no user")
    if t.get('first_name') != '': student.first_name = t.get('first_name')
    if t.get('last_name') != '': student.last_name = t.get('last_name')
    if t.get('birth_date') != '': student.birth_date = t.get('birth_date')

    # user.save()
    student.save()
    return HttpResponse("Edited Successfully!")

def remove_student(request):
    t = request.POST
    try:
        student = Student.objects.get(identity_code=t.get('national_id'))
    except:
        raise Http404("no user")
    student.delete()
    return HttpResponse("successfuliy removed")
