from django import forms
from .models import *


# тестовые формы, которые НЕ интересуют
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


# ГЛАВНЫЕ РАБОЧИЕ формы, которые интересуют
class Ext_Students_Form(forms.ModelForm):
    class Meta:
        model = Ext_Students
        exclude = ["id"]
        # fields = ["surname", "name", "middle_name", "work_position", "diplom", "education_year", "contract_expire", ]


class Education_Form(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ["id"]


# ВСПОМОГАТЕЛЬНЫЕ формы для словарей
class Academy_rank_form(forms.ModelForm):
    class Meta:
        model = Academy_rank
        fields = ['academy_rank_name']


class PHD_form(forms.ModelForm):
    class Meta:
        model = PHD
        fields = ['phd_name']


class Chair_form(forms.ModelForm):
    class Meta:
        model = Chair
        fields = ['chair_name']


class University_form(forms.ModelForm):
    class Meta:
        model = University
        fields = ['university_name']


class Realisation_form_form(forms.ModelForm):  # простите меня, потомки, за это название.
    class Meta:
        model = Realization_form
        fields = ['realization_form_name']


class Course_type_form(forms.ModelForm):
    class Meta:
        model = Course_type
        fields = ['course_type_name']
