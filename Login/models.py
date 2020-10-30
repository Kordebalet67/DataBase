from django.db import models
import mysql.connector
import pymysql

data_base = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="npo",
    cursorclass=pymysql.cursors.SSDictCursor
)

mycoursor = data_base.cursor()
mycoursor.execute("SELECT * FROM chair")
chair = mycoursor.fetchall()
mycoursor.execute("SELECT * FROM academy_rank")
academy_rank = mycoursor.fetchall()
mycoursor.execute("SELECT * FROM phd")
phd = mycoursor.fetchall()
mycoursor.execute("SELECT * FROM course_type")
course_type = mycoursor.fetchall()
mycoursor.execute("SELECT * FROM realisation_form")
realisation_form = mycoursor.fetchall()
mycoursor.execute("SELECT * FROM university")
university = mycoursor.fetchall()


class Users(models.Model):
    login = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Students(models.Model):
    name = models.TextField(max_length=30)
    surname = models.TextField(max_length=40)
    date_birth = models.DateField
    course = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s course %s" % (self.surname, self.name, self.course)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Courses(models.Model):
    course = models.CharField(max_length=10)

    def __str__(self):
        return self.course

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


# описание моделей словарей для таблицы students

list_chair = []
for i in range(len(chair)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_chair.append((chair[i]["id"], chair[i]["chair_name"]))

list_academy_rank = []
for i in range(len(academy_rank)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_academy_rank.append((academy_rank[i]["id"], academy_rank[i]["academy_rank_name"]))

list_phd = []
for i in range(len(phd)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_phd.append((phd[i]["id"], phd[i]["phd_name"]))


# print(chair[0]["chair_name"])  # самая важная хуйня во всём коде. из мускла сюда приходит список словарей. ИПАНУЦЦА
# print(list_chair)


class Chair(models.Model):
    id = models.IntegerField(primary_key=True)
    chair_name = models.CharField(max_length=100, choices=list_chair, default=None)

    def __str__(self):
        return self.chair_name


class PHD(models.Model):
    id = models.IntegerField(primary_key=True)
    phd_name = models.CharField(max_length=100, choices=list_phd, default=None)

    def __str__(self):
        return self.phd_name


class Academy_rank(models.Model):
    id = models.IntegerField(primary_key=True)
    academy_rank_name = models.CharField(max_length=100, choices=list_academy_rank, default=None)

    def __str__(self):
        return self.academy_rank_name


# описание моделей словарей для таблицы education
list_university = []
for i in range(len(university)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_university.append((university[i]["id"], university[i]["university_name"]))

list_course_type = []
for i in range(len(course_type)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_course_type.append((course_type[i]["id"], course_type[i]["course_type_name"]))

list_realisation_form = []
for i in range(len(realisation_form)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_realisation_form.append((realisation_form[i]["id"], realisation_form[i]["realisation_form_name"]))


class Realization_form(models.Model):
    id = models.IntegerField(primary_key=True)
    realization_form_name = models.CharField(max_length=100, choices=list_realisation_form, default=None)

    def __str__(self):
        return self.realization_form_name


class Course_type(models.Model):
    id = models.IntegerField(primary_key=True)
    course_type_name = models.CharField(max_length=100, choices=list_course_type, default=None)

    def __str__(self):
        return self.course_type_name


class University(models.Model):
    id = models.IntegerField(primary_key=True)
    university_name = models.CharField(max_length=100, choices=list_university, default=None)

    def __str__(self):
        return self.university_name


# описание главных моделей

class Ext_Students(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=45)
    surname = models.TextField(max_length=45)
    middle_name = models.TextField(max_length=45)
    work_position = models.TextField(max_length=255)
    diplom = models.TextField(max_length=511)
    contract_expire = models.IntegerField()
    education_year = models.IntegerField()
    fired = models.BooleanField()
    chair = Chair
    phd = PHD
    academy_rank = Academy_rank

    def __str__(self):
        return "%s %s %s" % (self.surname, self.name, self.middle_name)


class Education(models.Model):
    id = models.IntegerField(primary_key=True)
    university_text = models.TextField(max_length=511)
    course_name = models.TextField(max_length=511)
    course_start = models.DateField()
    course_end = models.DateField()
    info = models.TextField(max_length=1023)
    realisation_form = Realization_form
    chair = Chair
    student = Ext_Students
    course = Course_type
    university = University

    def __str__(self):
        return "%s %s %s" % (self.course_name, self.course_start, self.course_end)
