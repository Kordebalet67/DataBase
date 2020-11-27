from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from Login import views

urlpatterns = [

    url(r'^main_user', views.mainpage_user, name='Main Page'),
    url(r'^main', views.mainpage, name='Main Page'),
    url(r'^base', views.base, name='Base'),
    url(r'^educ', views.insert_education, name='Education'),
    url(r'^search', views.search, name='Search'),
    url(r'^upd', views.update, name='Update'),
    url(r'^del', views.delete, name='Delete'),
    url(r'^', views.auth, name='authorization'),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
