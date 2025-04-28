# check_sheet/urls.py
from django.urls import path
from . import views

app_name = 'check_sheet'

urlpatterns = [
    path(app_name + '/create/', views.create_check_sheet, name='create_check_sheet'),  # チェックシート作成ページ
]
