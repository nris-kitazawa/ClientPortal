from functools import wraps
from django.http import HttpResponseForbidden
from core.functions.userCheckHelper import is_guest_user

def guest_forbidden(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if is_guest_user(user):
            return HttpResponseForbidden("ゲストユーザーはこの操作を許可されていません。")
        return view_func(request, *args, **kwargs)
    return _wrapped_view