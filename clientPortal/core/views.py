# clientPortal/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

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
    return redirect('login')  # ログインページなどにリダイレクト

