# check_sheet/urls.py
from django.urls import path
from . import views

app_name = "check_sheet"

urlpatterns = [
    path("", views.check_sheet_top, name="top"),
    path("create/", views.create_check_sheet, name="create"),
    path("detail/<int:pk>/", views.check_sheet_detail, name="detail"),
    path("edit/<int:pk>/", views.edit_check_sheet, name="edit"),
    path("search/", views.check_sheet_top, name="search"),  # 検索もトップビューで処理
]
