from django.shortcuts import render
from django.utils import http
from django import http
from .forms import *
import mysql.connector

data_base = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="npo",
)

mycoursor = data_base.cursor()


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
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        courses = Courses.objects.filter(course=data["course"])

        return render(request, 'results/rescourse.html', locals())

    return render(request, 'search/scourse.html', locals())


def name(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        students = Students.objects.filter(surname=data["surname"])

        return render(request, 'results/resname.html', locals())

    return render(request, 'search/sname.html', locals())


def rescourse(request):
    courses = Courses.objects.all()
    return render(request, 'results/rescourse.html', locals())


def resname(request):
    students = Students.objects.all()
    return render(request, 'results/resname.html', locals())


def insert(request):
    insert_form = Ext_Students_Form(request.POST or None)
    chair_form = Chair_form
    phd_form = PHD_form
    academy_rank_form = Academy_rank_form

    if request.method == "POST" and insert_form.is_valid():
        data = insert_form.cleaned_data  # принимаем значение с ёбанной заполняемой формы
        chosen_chair = request.POST.get('chair_name')  # принимаем значение с ёбанного выпадающего списка №1
        chosen_academy_rank = request.POST.get('academy_rank_name')  # значение с ёбанного выпадающего списка №2
        chosen_phd = request.POST.get('phd_name')  # значение с ёбанного выпадающего списка №3

        sql = "insert into npo.students (surname, name, middle_name, work_position, diplom, contract_expire, education_year, chair, phd, academy_rank) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data["surname"], data["name"], data["middle_name"], data["work_position"], data["diplom"],
               data["contract_expire"], data["education_year"], chosen_chair, chosen_phd, chosen_academy_rank)
        mycoursor.execute(sql, val)
        data_base.commit()

        print(mycoursor.rowcount, "record inserted")
        insert_form.clean()
        return http.HttpResponseRedirect('')
    return render(request, 'insert/insert.html', locals())
