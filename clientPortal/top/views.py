# views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import render

# ログインページを表示するためにLoginViewを利用
class CustomLoginView(LoginView):
    template_name = 'login.html'  # ログインフォームのテンプレート

from django.contrib.auth.decorators import login_required

@login_required
def top_page(request):
    # ログインユーザーのグループを確認
    if request.user.groups.filter(name='NRIS').exists():
        # NRISユーザーの場合
        return render(request, 'nris_top.html')  # NRISユーザー用のトップページに遷移
    elif request.user.groups.filter(name='ゲスト').exists():
        # クライアントユーザーの場合
        return render(request, 'guest_top.html')  # クライアントユーザー用のトップページに遷移
    else:
        # その他のユーザー（エラー表示）
        return render(request, 'error_page.html')  # エラーページを表示
    
    
