from django.shortcuts import render, redirect
from django.utils import http
from django import http
from .forms import *
import mysql.connector
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission, User
from django.shortcuts import get_object_or_404

#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
#  обращение к базе mysql
data_base = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="npo",
)

mycoursor = data_base.cursor()


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы авторизации
def auth(request):
    form = UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():

        data = form.cleaned_data
        user = authenticate(username=data["login"], password=data["password"])
        if user is not None:
            login(request, user)
            if data["login"] == "user1":
                return mainpage_user(request)
            elif data["login"] == "Admin":
                return mainpage(request)

    return render(request, 'auth/logged_in.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод главной страницы с правами администратора
def mainpage(request):
    if not request.user.is_authenticated:
        return auth(request)
    if not request.user.username == "Admin":
        return auth(request)
    print(request.user.username)
    return render(request, 'main/main_admin.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод главной страницы с правами пользователя
def mainpage_user(request):
    if not request.user.is_authenticated:
        return auth(request)
    return render(request, 'main/main_user.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод базовой страницы
def base(request):
    return render(request, 'base.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы ввода новой информации
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
    if id_stud[0] is None:
        stud = 1
    else:
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


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы поиска по ФИО
def search(request):
    insert_form = Ext_Students_Form(request.POST or None)

    if request.method == "POST":
        surname = request.POST.get('surname')  # принимаем значение с ёбанной заполняемой формы
        name = request.POST.get('name')
        middle_name = request.POST.get('middle_name')

        if middle_name == '' and name == '':

            sql_search = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                         "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                         "students.diplom, students.contract_expire, students.education_year, students.fired" \
                         " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s" \
                         " and students.chair = chair.id and students.phd = phd.id " \
                         "and students.academy_rank = academy_rank.id"
            val_search = (surname,)
            mycoursor.execute(sql_search, val_search)

        else:
            if middle_name == "":

                sql_search = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                             "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                             "students.diplom, students.contract_expire, students.education_year, students.fired" \
                             " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s " \
                             "and name = %s and students.chair = chair.id and students.phd = phd.id " \
                             "and students.academy_rank = academy_rank.id"
                val_search = (surname, name)
                mycoursor.execute(sql_search, val_search)

            else:

                sql_search = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                             "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                             "students.diplom, students.contract_expire, students.education_year, students.fired" \
                             " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s and name = %s" \
                             "and middle_name = %s and students.chair = chair.id and students.phd = phd.id " \
                             "and students.academy_rank = academy_rank.id"
                val_search = (surname, name, middle_name)
                mycoursor.execute(sql_search, val_search)

        results = mycoursor.fetchall()

        return render(request, 'search/search.html', locals())
    return render(request, 'search/search.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы обновления информации по ИД
#  -------------------------------------------------------------------------------------------------
# самая ёбань. совмещено сразу три формы
#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
def update(request):
    insert_form = Ext_Students_Form(request.POST or None)
    id_form = ID_choose_form(request.POST or None)
    education_form = Education_Form((request.POST or None))
    # перечисляем ёбанные формы для заполнения. ещё 6  - с ёбанными выпадающими списками
    university_form = University_form
    course_type_form = Course_type_form
    realisation_form_form = Realisation_form_form  # гореть мне в аду за такие названия
    chair_form = Chair_form
    phd_form = PHD_form
    academy_rank_form = Academy_rank_form

    if request.method == "POST":
        surname = request.POST.get('surname')  # принимаем значение с ёбанной заполняемой формы
        name = request.POST.get('name')
        middle_name = request.POST.get('middle_name')
        chosen_id = request.POST.get('id')

        if chosen_id is not None:
            print(chosen_id)

        else:
            if middle_name == '' and name == '':

                sql_update = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                             "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                             "students.diplom, students.contract_expire, students.education_year, students.fired," \
                             " students.id from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s" \
                             " and students.chair = chair.id and students.phd = phd.id " \
                             "and students.academy_rank = academy_rank.id"
                val_update = (surname,)
                mycoursor.execute(sql_update, val_update)

            else:
                if middle_name == "":

                    sql_update = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                                 "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                                 "students.diplom, students.contract_expire, students.education_year, students.fired" \
                                 " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s " \
                                 "and name = %s and students.chair = chair.id and students.phd = phd.id " \
                                 "and students.academy_rank = academy_rank.id"
                    val_update = (surname, name)
                    mycoursor.execute(sql_update, val_update)

                else:

                    sql_update = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                                 "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                                 "students.diplom, students.contract_expire, students.education_year, students.fired" \
                                 " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s and name = %s" \
                                 "and middle_name = %s and students.chair = chair.id and students.phd = phd.id " \
                                 "and students.academy_rank = academy_rank.id"
                    val_update = (surname, name, middle_name)
                    mycoursor.execute(sql_update, val_update)

            results = mycoursor.fetchall()

        return render(request, 'update/update.html', locals())
    return render(request, 'update/update.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы удаления студента
#  -------------------------------------------------------------------------------------------------
#  ТОЛЬКО ДЛЯ АДМИНА
#  -------------------------------------------------------------------------------------------------
def delete(request):
    insert_form = Ext_Students_Form(request.POST or None)
    id_form = ID_choose_form(request.POST or None)

    if request.method == "POST":
        surname = request.POST.get('surname')  # принимаем значение с ёбанной заполняемой формы
        name = request.POST.get('name')
        middle_name = request.POST.get('middle_name')
        chosen_id = request.POST.get('id')

        if chosen_id is not None:
            print(chosen_id)

            val_delete = (chosen_id,)

            sql_delete = "delete from education where education.student = %s"
            mycoursor.execute(sql_delete, val_delete)

            sql_delete = "delete from students where students.id = %s"
            mycoursor.execute(sql_delete, val_delete)

            data_base.commit()

        else:

            if middle_name == '' and name == '':

                sql_search_delete = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                                    "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                                    "students.diplom, students.contract_expire, students.education_year, students.fired," \
                                    " students.id from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s" \
                                    " and students.chair = chair.id and students.phd = phd.id " \
                                    "and students.academy_rank = academy_rank.id"
                val_search_delete = (surname,)
                mycoursor.execute(sql_search_delete, val_search_delete)

            else:
                if middle_name == "":

                    sql_search_delete = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                                        "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                                        "students.diplom, students.contract_expire, students.education_year, students.fired" \
                                        " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s " \
                                        "and name = %s and students.chair = chair.id and students.phd = phd.id " \
                                        "and students.academy_rank = academy_rank.id"
                    val_search_delete = (surname, name)
                    mycoursor.execute(sql_search_delete, val_search_delete)

                else:

                    sql_search_delete = "select students.surname, students.name, students.middle_name, chair.chair_name, " \
                                        "students.work_position, phd.phd_name, academy_rank.academy_rank_name," \
                                        "students.diplom, students.contract_expire, students.education_year, students.fired" \
                                        " from npo.students, npo.chair, npo.phd, npo.academy_rank where surname = %s and name = %s" \
                                        "and middle_name = %s and students.chair = chair.id and students.phd = phd.id " \
                                        "and students.academy_rank = academy_rank.id"
                    val_search_delete = (surname, name, middle_name)
                    mycoursor.execute(sql_search_delete, val_search_delete)

            results = mycoursor.fetchall()

        return render(request, 'delete/delete.html', locals())
    return render(request, 'delete/delete.html', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы обновления содержимого в словарях(выпадающих списках)
#  -------------------------------------------------------------------------------------------------
#  ТОЛЬКО ДЛЯ АДМИНА
#  -------------------------------------------------------------------------------------------------
def update_dicts(request):
    if not request.user.is_authenticated:
        return auth(request)
    if not request.user.username == "Admin":
        return auth(request)
    return render(request, '', locals())


#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# метод страницы обновления содержимого в словарях(выпадающих списках)
#  -------------------------------------------------------------------------------------------------
def add_educ(request):
    if not request.user.is_authenticated:
        return auth(request)
    return render(request, '', locals())


#
#
#
#
#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
# этот фрагмент отжил своё. но как работающий образец должен остаться
#  -------------------------------------------------------------------------------------------------
#  -------------------------------------------------------------------------------------------------
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


def update1(request):
    return render(request, 'update/update.html', locals())


def delete1(request):
    return render(request, 'delete/delete.html', locals())
