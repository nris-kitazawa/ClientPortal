# check_sheet/urls.py
from django.urls import path
from . import views

app_name = "check_sheet"

urlpatterns = [
    path("", views.check_sheet_top, name="top"),
    path("create/", views.create_check_sheet, name="create"),
    path("detail/<slug:id>/", views.check_sheet_detail, name="detail"),
    path("edit/<slug:id>/", views.edit_check_sheet, name="edit"),
    path("search/", views.check_sheet_top, name="search"),  # 検索もトップビューで処理
]
