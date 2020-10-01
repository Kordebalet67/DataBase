from django.db import models


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
        return self.surname

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
