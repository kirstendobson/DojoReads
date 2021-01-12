from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.books),
]