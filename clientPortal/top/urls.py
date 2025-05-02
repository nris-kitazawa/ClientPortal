# urls.py
from django.urls import path
from .views import top_page, root_page

app_name = "top"

urlpatterns = [
    path("", root_page, name="root_page"),
    path("top/", top_page, name="top"),
]
