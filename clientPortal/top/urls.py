# urls.py
from django.urls import path

# apps/check_sheet/urls.py
from .views import top_page

app_name = "top"

urlpatterns = [
    path("", top_page, name="root_redirect"),
    path("top/", top_page, name="top")
]
