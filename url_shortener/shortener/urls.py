from django.urls import path
from . import views

urlpatterns = [
    path('visit/<str:short>', views.home),
    path('register', views.register),
    path('login', views.login),
    path('generate', views.shorten),
    path('stat/<str:short>', views.stat)
]
