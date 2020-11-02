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
            return render(request, 'main/main.html', locals())

    return render(request, 'auth/auth.html', locals())


def mainpage(request):
    return render(request, 'main/main.html', locals())


def base(request):
    return render(request, 'base.html', locals())


def update(request):
    return render(request, 'update/update.html', locals())


def delete(request):
    return render(request, 'delete/delete.html', locals())


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


def insert_education(request):
    # перечисляем ёбанные формы для заполнения. 2 формы - с обычными текстовыми полями
    insert_form = Ext_Students_Form(request.POST or None)
    education_form = Education_Form((request.POST or None))
    # перечисляем ёбанные формы для заполнения. ещё 6  - с ёбанными выпадающими списками
    university_form = University_form
    course_type_form = Course_type_form
    realisation_form_form = Realisation_form_form  # гореть мне в аду за такие названия
    chair_form = Chair_form
    phd_form = PHD_form
    academy_rank_form = Academy_rank_form

    mycoursor.execute("SELECT max(id) FROM npo.students")  # получение id слздаваемого студента
    id_stud = mycoursor.fetchone()

    stud = (id_stud[0]) + 1
    if request.method == "POST" and insert_form.is_valid() and education_form.is_valid():
        data = insert_form.cleaned_data  # принимаем значение с ёбанной заполняемой формы студентов
        data_ed = education_form.cleaned_data  # принимаем значение с ёбанной заполняемой формы учёбы

        chosen_chair = request.POST.get('chair_name')  # принимаем значение с ёбанного выпадающего списка №1
        chosen_academy_rank = request.POST.get('academy_rank_name')  # значение с ёбанного выпадающего списка №2
        chosen_phd = request.POST.get('phd_name')  # значение с ёбанного выпадающего списка №3
        chosen_university = request.POST.get('university_name')  # значение с ёбанного выпадающего списка №4
        chosen_course_type = request.POST.get('course_type_name')  # значение с ёбанного выпадающего списка №5
        chosen_realisation_form = request.POST.get('realisation_form_name')  # значение с ёбанного выпадающего списка №6
        print(stud)
        # запихиваем все полученные значения из форм по таблицам и словарям
        sql_stud = "insert into npo.students (surname, name, middle_name, work_position, diplom, contract_expire, " \
                   "education_year, chair, phd, academy_rank) " \
                   "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val_stud = (data["surname"], data["name"], data["middle_name"], data["work_position"], data["diplom"],
                    data["contract_expire"], data["education_year"], chosen_chair, chosen_phd, chosen_academy_rank)

        mycoursor.execute(sql_stud, val_stud)
        data_base.commit()

        sql_ed = "insert into npo.education (student, course_type, university, university_text, course_name, " \
                 "course_start, course_end, realisation_form, chair, info)" \
                 "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val_ed = (stud, chosen_course_type, chosen_university, data_ed["university_text"], data_ed["course_name"],
                  data_ed["course_start"], data_ed["course_end"], chosen_realisation_form, chosen_chair,
                  data_ed["info"])

        mycoursor.execute(sql_ed, val_ed)
        data_base.commit()

        print(mycoursor.rowcount, "record inserted")
        return http.HttpResponseRedirect('')
    return render(request, 'insert/insert_education.html', locals())


def search(request):
    return render(request, 'search/search.html', locals())


# этот фрагмент отжил своё. но как работающий образец должен остаться
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

        sql_stud = "insert into npo.students (surname, name, middle_name, work_position, diplom, contract_expire, " \
                   "education_year, chair, phd, academy_rank) " \
                   "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val_stud = (data["surname"], data["name"], data["middle_name"], data["work_position"], data["diplom"],
                    data["contract_expire"], data["education_year"], chosen_chair, chosen_phd, chosen_academy_rank)

        mycoursor.execute(sql_stud, val_stud)
        data_base.commit()

        print(mycoursor.rowcount, "record inserted")
        return http.HttpResponseRedirect('')
    return render(request, 'insert/insert.html', locals())
