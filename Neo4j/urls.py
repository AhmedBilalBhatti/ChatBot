from django.conf.urls import handler404
from django.urls import path, include
from .import views
from Neo4j import *

urlpatterns = [
    path('', views.signup, name='signup'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('forget', views.forget, name='forget'),
    path('forget', views.forget, name='forget'),
    path('forget2', views.forget2, name='forget2'),
    path('forget3', views.forget3, name='forget3'),
    path('upload_pic', views.upload_pic, name='upload_pic'),
    path('contact',views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('help', views.help, name='help'),
    path('chat', views.chat, name='chat'),
    path('history', views.history, name='history'),
    path('vi', views.vi, name='vi'),
]

handler404 = 'Neo4j.views.error_404'