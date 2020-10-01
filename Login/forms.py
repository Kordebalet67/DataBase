from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = [""]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ["surname", "name"]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        exclude = [""]
