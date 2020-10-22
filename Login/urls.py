from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from Login import views

urlpatterns = [

    url(r'^main', views.mainpage, name='MainPage'),
    url('^search/sname.html', views.name, name='Search by name'),
    url(r'^search/scourse.html', views.course, name='Search by course'),
    url(r'^results/rescourse.html', views.rescourse, name='Results of searching by course'),
    url(r'^results/resname.html', views.resname, name='Results of searching by name'),
    url(r'^insert/insert.html', views.insert, name='Insert'),
    url(r'^', views.auth, name='authorization'),

]
