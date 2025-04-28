# checksheets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('/create_checksheet/', views.create_checksheet, name='create_checksheet'),
    path('client/<str:link>/', views.client_survey, name='client_survey')
]