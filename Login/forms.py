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


class Ext_Students_Form(forms.ModelForm):
    class Meta:
        model = Ext_Students
        exclude = ["id"]
        # fields = ["surname", "name", "middle_name", "work_position", "diplom", "education_year", "contract_expire", ]


class Education_Form(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ["id"]


class Academy_rank_form(forms.ModelForm):
    model = forms.MultipleChoiceField(choices=Academy_rank.objects.all())
    exclude = ["id"]


class PHD_form(forms.ModelForm):
    model = forms.MultipleChoiceField(choices=PHD.objects.all())
    exclude = ["id"]


class Chair_form(forms.ModelForm):
    class Meta:
        model = Chair
        fields = ['chair_name']
