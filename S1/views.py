from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, PackageLoader, select_autoescape
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from S1 import models
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login

# Create your views here.
from S1.models import Person
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
        if t['national_id'] == '' or t['first_name'] == '' or t['last_name'] == '' or t['birth_date'] == '':
            raise Http404("hame mawared")
        if Person.objects.filter(identity_code=t['national_id']).exists():
            raise Http404("user tekrari")
        print(t['birth_date'])
        user = User.objects.create(username=t.get('user_name')
                                   , password=t.get('password')
                                   , email=t.get('email')
                                   , first_name=t.get('first_name')
                                   , last_name=t.get('last_name'))

        person = Person.objects.create(identity_code=t.get('national_id'),
                                       user=user,
                                       last_name=t.get('last_name'),
                                       birth_date=date_parser(t.get('birth_date')))

        return HttpResponse('successful sign up')


# def represent_student_list(request):
#     student_list = Student.objects.all()
#     env = Environment(loader=PackageLoader('S1', 'Web/templates'))
#     env.globals.update({'static': staticfiles_storage.url("S1/"), 'url': reverse})
#     template = env.get_template('list.html')
#     data = {'header': ['نام', 'نام خانوادگی', 'تاریخ تولد', 'شماره شناسنامه'],
#             'body': [],
#             }
#     for s in student_list:
#         list = data['body']
#         list.append([s.first_name, s.last_name, s.birth_date, s.identity_code])
#     list_content = template.render(data=data)
#     return HttpResponse(list_content)

def show_main_page(request):
    env = Environment(loader=PackageLoader('S1', 'Web/templates'))
    env.globals.update({'static': staticfiles_storage.url("S1/"), 'url': reverse})
    template = env.get_template('main.html')


def edit_student_info(request):
    t = request.POST
    try:
        user = User.objects.get(username=t['user_name'])
    except:
        raise Http404("no user")

    person = user.person
    if t.get('first_name') != '': user.first_name = t.get('first_name')
    if t.get('last_name')  != '': user.last_name = t.get('last_name')
    if t.get('birth_date') != '': person.birth_date = t.get('birth_date')

    user.save()
    person.save()
    return HttpResponse("Edited Successfully!")


def remove_student(request):
    t = request.POST
    try:
        user = User.objects.get(username=t.get('user_name'))
    except:
        raise Http404("no user")
    person = user.person
    person.delete()
    return HttpResponse("successfuliy removed")


def sign_in(request):
    if request.method is 'POST':
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('successful login')
            else:
                return HttpResponse('unsuccessful login')
        except:
            raise Http404("problem in sending data")


def process_creation(request):
    # get person - > manager
    manager = ...
    process_name = ...
    f_phase = ...
    process = models.Process.objects.create(name=process_name,
                                            start_phase=f_phase)
    process.save()


from anytree import Node


def get_process(request):
    process_name = ...
    process = models.Process.objects.get(name=process_name)
    phase_list = []
    f_phase = process.start_phase
    tree = Node(f_phase)
    make_tree(tree, f_phase)
    pass


def make_tree(node, f_phase):
    if not f_phase.is_finish:
        acc_phase = f_phase.next_phase_acc.s_phase
        rej_phase = f_phase.next_phase_rej.s_phase
        make_tree(Node(acc_phase, parent=f_phase), acc_phase)
        make_tree(Node(rej_phase, parent=f_phase), rej_phase)


def phase_creation(request):
    phase_type = ...
    phase = models.Phase.objects.create(phase_type=phase_type)
    phase.save()


def get_phase_types(request):
    models.PhaseType.objects.all()


def get_accountant_cartable(request):
    pass


def get_phase(request):
    id = ...
    phase = models.Phase.objects.get(id=id)


def verify_phase(request):
    id = ...
    phase = models.Phase.objects.get(id=id)
    phase.is_verified = True
    phase.save()


def get_processes_student(request):
    models.Process.objects.all()


def get_process_student(request):
    proc_name = ...
    models.Process.objects.get(name=proc_name)


def create_phase_rel(request):
    f_phase = ...
    s_phase = ...
    is_acc = ...
    rel = models.PairPhase.objects.create(f_phase=f_phase, s_phase=s_phase, is_acc=is_acc)


def get_start_phase(request):
    pass


def get_next_phase(request):
    pass


def upload_attachment(request):
    file = ...
    title = ...
    attachment = models.Attachment.objects.create(file=file, title=title)
    attachment.save()


def pay(request):
    pass


def submit_data(request):
    pass


def get_main_page(request):
    pass
