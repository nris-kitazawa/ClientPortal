from django.shortcuts import redirect
from django.conf import settings

EXEMPT_URLS = [  # ログイン不要なURLをここに追加
    '/login/',
    '/admin/login/',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if not request.user.is_authenticated and path not in EXEMPT_URLS:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
    
from django.http import HttpResponseForbidden

class GuestAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # ゲストでログインしている場合
        if user.is_authenticated and getattr(user, 'is_guest', False):
            # アクセス先パスが /guest/ で始まっていなければ禁止
            if not request.path.startswith('/guest/'):
                return HttpResponseForbidden("ゲストはこのページにアクセスできません。")

        return self.get_response(request)

