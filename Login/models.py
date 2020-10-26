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


# описание моделей словарей

list_chair = []
for i in range(len(chair)):  # запихиваем ёбанные значения из списка словарей в список ёбанных кортежей
    list_chair.append((chair[i]["id"], chair[i]["chair_name"]))


# print(chair[0]["chair_name"])  # самая важная хуйня во всём коде. из мускла сюда приходит список словарей. ИПАНУЦЦА
# print(list_chair)


class Chair(models.Model):
    id = models.IntegerField(primary_key=True)
    chair_name = models.CharField(max_length=100, choices=list_chair, default=chair[0])

    def __str__(self):
        return self.chair_name


class Realization_form(models.Model):
    id = models.IntegerField(primary_key=True)
    realization_form_name = models.TextField(max_length=511)

    def __str__(self):
        return self.realization_form_name


class Course_type(models.Model):
    id = models.IntegerField(primary_key=True)
    course_type_name = models.TextField(max_length=511)

    def __str__(self):
        return self.course_type_name


class University(models.Model):
    id = models.IntegerField(primary_key=True)
    university_name = models.TextField(max_length=511)

    def __str__(self):
        return self.university_name


class PHD(models.Model):
    id = models.IntegerField(primary_key=True)
    phd_name = models.TextField(max_length=127)

    def __str__(self):
        return self.phd_name


class Academy_rank(models.Model):
    id = models.IntegerField(primary_key=True)
    academy_rank_name = models.TextField(max_length=45)

    def __str__(self):
        return self.academy_rank_name


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
    student = Ext_Students
    course = Course_type
    university = University
    university_text = models.TextField(max_length=511)
    course_name = models.TextField(max_length=511)
    course_start = models.DateField
    course_end = models.DateField
    realisation_form = Realization_form
    chair = Chair
    info = models.TextField(max_length=1023)

    def __str__(self):
        return "%s %s %s" % (self.course_name, self.course_start, self.course_end)
