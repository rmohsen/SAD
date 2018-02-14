from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, PackageLoader, select_autoescape
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from S1 import forms
from S1 import models
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm, SignInForm

# Create your views here.
from S1.models import Person, Phase, Process, PhaseType, Position, Student
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


def auth_register(input):
    # post
    # try:
    t = input
    if User.objects.filter(username=t['username']).exists():
        return 0
    user = User.objects.create(username=t.get('username')
                               , password=t.get('password')
                               , email=t.get('email')
                               , first_name=t.get('first_name')
                               , last_name=t.get('last_name'))
    user.save()
    if t.get('type') == 'S':
        student = Student.objects.create(user=user, identity_code=t['identity_code'])
        student.save()
    else:
        person = Person.objects.create(user=user, identity_code=t.get('identity_code'))
        person.save()
    return 1


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
        list.append([s.first_name, s.last_name, s.birth_date, s.identity_code])
    list_content = template.render(data=data)
    return HttpResponse(list_content)


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
    if t.get('last_name') != '': user.last_name = t.get('last_name')
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
    return HttpResponse("successfully removed")


def sign_in(request, input):
    try:
        user = authenticate(input, username=input['username'], password=input['password'])
        if user is not None:
            login(request=request, user=user)
            return 1
        else:
            return 0
    except:
        raise Http404("problem in sending data")


def process_creation(request):
    # put some thing in session put some in post
    s = request.session
    t = request.POST
    p = User.objects.get(s['user_name']).person
    if p.position != "Manager":
        return Http404("you have no permission")
    # get person -> manager
    manager = p
    process_name = t['process_name']
    f_phase = Phase.objects.get(t['phase_id'])
    process = models.Process.objects.create(name=process_name,
                                            start_phase=f_phase)
    process.save()


from anytree import Node


def get_process(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.process_form(request.POST)
        t = request.POST
        process_info = Process.objects.get(id=t['process_id'], name=t['name'])
        # check whether it's valid:
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        return render(request, 'test_vis_process.html', {'data': process_info})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.process_form()

    return render(request, 'test_get_process.html', {'form': form})

    # process_name = request.POST['process_name']
    # process = models.Process.objects.get(name=process_name)
    # f_phase = process.start_phase
    # tree = Node(f_phase)
    # make_tree(tree, f_phase)
    # return tree


def make_tree(node, f_phase):
    if not f_phase.is_finish:
        acc_phase = f_phase.next_phase_acc.s_phase
        rej_phase = f_phase.next_phase_rej.s_phase
        make_tree(Node(acc_phase, parent=f_phase), acc_phase)
        make_tree(Node(rej_phase, parent=f_phase), rej_phase)


def phase_creation(request):
    phase_type = PhaseType.objects.get(request.POST['phase_type_id'])
    phase = models.Phase.objects.create(phase_type=phase_type)
    phase.save()


def show_phase(request):
    form = forms.phase_form(request.POST)
    form1 = forms.main_form(request.POST)
    if form.is_valid():
        return render(request, 'test_vis_phase.html',
                      {'data': Phase.objects.get(id=request.POST.get('phase_id')), 'form': form1})
    else:
        form = forms.phase_form()
    return render(request, 'test_show_phase.html', {'form': form})


def show_phase_type(request):
    form = forms.phase_type_form(request.POST)
    if form.is_valid():
        return render(request, 'test_vis_phase_type.html',
                      {'data': Phase.objects.get(name=request.POST.get('name'))})
    else:
        form = forms.phase_type_form()
    return render(request, 'test_show_phase_type.html', {'form': form})


def get_phase_types(request):
    models.PhaseType.objects.all()


def create_process_type(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.process_type_form(request.POST)
        t = request.POST
        models.ProcessType.objects.create(name=t['name'],
                                          start_phase_type=PhaseType.objects.get(id=t['first_phase_type_id']))

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.process_type_form()
    return render(request, 'test_add_process_type.html', {'names': 'c', 'form': form})


def get_transactions(request):
    transactions = [{'amount': '1', 'issue_tracking_number': '2', 'date': '3', 'account_id': '4'}]
    return render(request, 'test_get_transactions.html', {'transactions': transactions})


def create_phase_type(request):
    if request.method == 'POST':
        form1 = forms.phase_type_form(request.POST)
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if form1.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            t = request.POST
            PhaseType.objects.create(name=t['name'],
                                     next_phase_type_acc=t['next_phase_type_acc'],
                                     next_phase_type_rej=t['next_phase_type_rej'],
                                     need_attachment=t['need_attachment'],
                                     need_transaction=t['need_transaction'])
            return HttpResponseRedirect('/test_karbari_modir/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form1 = forms.phase_type_form()

    return render(request, 'test_add_phase_type.html', {'form': form1})


#
# def show_phase_types(request):
#     proc = [{'id': '100', 'need_transaction': 'True', 'need_attachment': 'false'}, 'prc2', 'prc3']
#     return render(request, 'show_phase_type_page.html', {'names': proc})

def show_account_cartable(request):
    # cartable = get_accountant_cartable()
    person = Person.objects.get(user__username=User.get_username(request))
    cartables = Phase.objects.filter(phase_type__accountant_position__person=person).all()
    return render(request, 'test_show_cartable.html', {'cartables': cartables})


def get_phase(request):
    id = request.POST['phase_id']
    phase = models.Phase.objects.get(id=id)


def verify_phase(request):
    id = request.session['phase_id']
    phase = models.Phase.objects.get(id=id)
    phase.is_verified = True
    phase.save()


def get_processes_student(request):
    models.Process.objects.all()
    return show_processes(...)


def get_process_student(request):
    proc_name = Process.objects.get(name=request.POST['process_name'])
    models.Process.objects.get(name=proc_name)


def get_start_phase(request):
    s = request.session
    pass


def get_next_phase(request):
    pass


def upload_attachment(request):
    file = request.FILES
    title = request.POST
    attachment = models.Attachment(file=file, title=title)
    if attachment.is_valid():
        handle_uploaded_file(request.FILES['file'])
        return ...
    attachment.save()


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def pay(request):
    pass


def submit_data(request):
    pass


def get_main_page(request):
    return render(request, 'main_page.html')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if auth_register(request.POST) == 1:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/test/')
        else:
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'reg_form.html', {'form': form})


def get_signin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)
        sign_in(request=request, input=request.POST)
        if Student.objects.filter(user__username=request.POST['username']).exists():
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('/test_karbari/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignInForm()

    return render(request, 'signin_form.html', {'form': form})


def get_signin_modir(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)
        sign_in(request=request, input=form.request.POST)
        # check whether it's valid:)
        if Position.objects.filter(person__user__username=request.POST['username']).exists():
            if Position.objects.get(person__user__username=request.POST['username']).title == 'Manager':
                if form.is_valid():
                    # process the data in form.cleaned_data as required
                    # ...
                    # redirect to a new URL:
                    return HttpResponseRedirect('/test_karbari_modir/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignInForm()

    return render(request, 'test_signin_modir.html', {'form': form})


def get_signin_acc(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)
        sign_in(request=request, input=request.POST)
        if Position.objects.filter(person__user__username=request.POST['username']).exists():
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('/test_karbari_acc/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignInForm()

    return render(request, 'test_signin_acc.html', {'form': form})


def get_modir_karbari(request):
    return render(request, 'test_karbari_modir.html')


def get_processes(request):
    return render(request, 'test_get_processes.html')


def get_student_karbari(request):
    return render(request, 'test_karbari.html')


def get_acc_karbari(request):
    return render(request, 'test_karbari_acc.html')


def show_process(request):
    form = forms.process_form(request.POST)
    if form.is_valid():
        return render(request, 'test_vis_process.html',
                      {'data': Process.objects.get(request.POST.get('name'))})
    else:
        form = forms.process_form()
    return render(request, 'test_show_process.html', {'form': form})


def show_processes(request):
    proc = [{'name': 'a1', 'type': 'a2', 'id': 'a3'}, {'f1': 'b2', 'f2': 'b2', 'f3': 'b3'}]
    proc = Process.objects.all()
    # proc = get_processes()
    return render(request, 'test_get_processes.html', {'data': stu})
