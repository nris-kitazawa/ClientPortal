# urls.py
from django.urls import path
from .views import CustomLoginView

# apps/check_sheet/urls.py
from .views import top_page

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # ログインURL
    path('top/', top_page, name='top'),  # TOP画面URL
]
