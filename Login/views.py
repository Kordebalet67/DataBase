from django.shortcuts import render
from .forms import *


def auth(request):
    form = UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():

        data = form.cleaned_data
        if data["login"] == "user" and data["password"] == "Qwerty":
            return render(request, 'main/mainPage.html', locals())

    return render(request, 'auth/auth.html', locals())


def mainpage(request):
    return render(request, 'main/mainPage.html', locals())


def course(request):
    return render(request, 'search/scourse.html', locals())


def name(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST":

        return render(request, 'results/resname.html', locals())

    return render(request, 'search/sname.html', locals())


def rescourse(request):
    return render(request, 'results/rescourse.html', locals())


def resname(request):
    return render(request, 'results/resname.html', locals())
