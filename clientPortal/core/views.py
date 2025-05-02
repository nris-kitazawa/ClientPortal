# clientPortal/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from core.functions.decorator import guest_forbidden
from core.functions.userCheckHelper import is_guest_user

@guest_forbidden
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/top/")
        else:
            messages.error(request, "ログイン情報が正しくありません。")
    return render(request, "login.html")

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # セッションデータと認証情報をすべて削除
    return redirect('/')  # ログインページなどにリダイレクト

from django.shortcuts import render, redirect
from django.urls import reverse


def guest_login_view(request):
    next_url = request.GET.get('next')
    id = None
    error = None
    error_message = "ゲストユーザーが存在しないまたはパスワードが正しくありません。"

    if not next_url:
        return redirect(reverse('top:root_page'))

    # nextパラメータからuuidを抽出（例: /edit/uuid）
    if next_url.startswith('check_sheet/edit/'):
        id = next_url.split('check_sheet/edit/')[1].strip('/')
        next_url = request.scheme + '://' + request.get_host() + "/guest/" + next_url

    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=id, password=password)
        if user and is_guest_user(user):
            login(request, user)
            return redirect(next_url)
        else:
            error = error_message

    return render(request, 'guest_login.html', {'uuid': id, 'error': error, 'next': next_url})