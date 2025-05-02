# clientPortal/urls.
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path("guest/login/", views.guest_login_view, name='guest_login'),
    path('logout/', views.logout_view, name='logout'),
]
