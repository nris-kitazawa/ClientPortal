# checksheets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('nris/login/', views.nris_login, name='nris_login'),
    path('nris/dashboard/', views.nris_dashboard, name='nris_dashboard')
]