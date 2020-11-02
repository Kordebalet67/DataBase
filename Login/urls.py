from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from Login import views

urlpatterns = [

    url(r'^main', views.mainpage, name='MainPage'),
    url('^search/sname.html', views.name, name='Search by name'),
    url(r'^search/scourse.html', views.course, name='Search by course'),
    url(r'^insert/insert.html', views.insert, name='Insert'),
    url(r'^base', views.base, name='Base'),
    url(r'^educ', views.insert_education, name='Education'),
    url(r'^search', views.search, name='Search'),
    url(r'^', views.auth, name='authorization'),

]
