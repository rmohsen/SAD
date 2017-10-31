from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Template
# Create your views here.


def index(request):
    return HttpResponse("<html><body>Hello guys!</body></html>")
