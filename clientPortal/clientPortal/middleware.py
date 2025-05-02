from django.shortcuts import redirect
from core.functions.userCheckHelper import is_guest_user
from django.http import HttpResponseForbidden

EXEMPT_URLS = [  # ログイン不要なURLをここに追加
    "/",
    '/login/',
    '/admin/login/',
    '/guest/login/',
    "/logout/",
    '/favicon.ico',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path in EXEMPT_URLS:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return HttpResponseForbidden("このページにアクセスできません。")
    
        if is_guest_user(request.user):
            # アクセス先パスが /guest/ で始まっていなければ禁止
            if not request.path.startswith('/guest/'):
                return HttpResponseForbidden("ゲストはこのページにアクセスできません。")

        return self.get_response(request)