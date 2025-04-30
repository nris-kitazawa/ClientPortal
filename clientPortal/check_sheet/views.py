# check_sheet/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CheckSheetForm
from .models import CheckSheet
import random
import string

def generate_password(length=8):
    """ランダムなパスワードを生成する関数"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def create_check_sheet(request):
    if request.method == 'POST':
        form = CheckSheetForm(request.POST)
        if form.is_valid():
            # チェックシートを保存
            check_sheet = form.save(commit=False)
            check_sheet.password = generate_password()  # ゲスト用のパスワードを生成
            check_sheet.created_by = request.user
            check_sheet.save()

            # 成功メッセージを表示
            messages.success(request, 'チェックシートが作成されました！')

            # ゲスト用リンクとパスワードを表示するページに遷移
            return render(request, 'check_sheet_created.html', {'check_sheet': check_sheet})
    else:
        form = CheckSheetForm()

    return render(request, 'create_check_sheet.html', {'form': form})

# check_sheet/views.py
from django.shortcuts import render, get_object_or_404
from .models import CheckSheet
from .forms import CheckSheetAnswerForm

def guest_answer(request, check_sheet_id):
    # ゲストユーザー用にチェックシートを取得
    check_sheet = get_object_or_404(CheckSheet, pk=check_sheet_id)
    
    if request.method == 'POST':
        form = CheckSheetAnswerForm(request.POST)
        if form.is_valid():
            # 回答を保存する処理
            form.save()
            
            # 回答が送信されたら、NRISユーザーに通知
            # ここで、通知を送る処理（例えば、メールなど）を追加できます
            
            return render(request, 'thank_you.html', {'check_sheet': check_sheet})
    else:
        form = CheckSheetAnswerForm()

    return render(request, 'guest_answer.html', {'check_sheet': check_sheet, 'form': form})

# check_sheet/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import CheckSheet

def check_sheet_index(request):
    check_sheets = CheckSheet.objects.filter(user=request.user)  # NRISユーザーが作成したチェックシート
    return render(request, 'check_sheet_index.html', {'check_sheets': check_sheets})

def delete_check_sheet(request, check_sheet_id):
    check_sheet = get_object_or_404(CheckSheet, pk=check_sheet_id, user=request.user)
    check_sheet.delete()
    return redirect('check_sheet:index')

# check_sheet/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CheckSheet, CheckSheetAnswer
from .forms import CheckSheetAnswerForm

def check_sheet_answer(request, check_sheet_id):
    check_sheet = CheckSheet.objects.get(id=check_sheet_id)
    
    if request.method == 'POST':
        form = CheckSheetAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user  # 現在のユーザーを設定
            answer.save()
            # 送信後、NRISユーザーに通知を送信するコードを追加することができます
            return redirect('check_sheet:top')  # チェックシートのトップページにリダイレクト
    else:
        form = CheckSheetAnswerForm()

    return render(request, 'answer.html', {'form': form, 'check_sheet': check_sheet})

from django.shortcuts import render, redirect, get_object_or_404
from .models import CheckSheet
from .forms import CheckSheetForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def check_sheet_top(request):
    form = CheckSheetForm()
    my_sheets = CheckSheet.objects.filter(created_by=request.user)

    # 閲覧履歴（例: セッションに保存されているIDリスト）
    viewed_ids = request.session.get("viewed_check_sheets", [])
    viewed_sheets = CheckSheet.objects.filter(id__in=viewed_ids)

    # 検索処理
    q = request.GET.get("q")
    search_results = CheckSheet.objects.filter(title__icontains=q) if q else []

    context = {
        "form": form,
        "my_sheets": my_sheets,
        "viewed_sheets": viewed_sheets,
        "search_results": search_results,
    }
    return render(request, "check_sheet_top.html", context)

from django.shortcuts import render, get_object_or_404
from .models import CheckSheet
from django.contrib.auth.decorators import login_required

def check_sheet_detail(request, pk):
    check_sheet = get_object_or_404(CheckSheet, pk=pk)
    return render(request, "check_sheet/check_sheet_detail.html", {"check_sheet": check_sheet})

from .forms import CheckSheetForm
from django.shortcuts import redirect

def edit_check_sheet(request, pk):
    check_sheet = get_object_or_404(CheckSheet, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = CheckSheetForm(request.POST, instance=check_sheet)
        if form.is_valid():
            form.save()
            return redirect("check_sheet:detail", pk=check_sheet.pk)
    else:
        form = CheckSheetForm(instance=check_sheet)

    return render(request, "check_sheet/edit_check_sheet.html", {"form": form, "check_sheet": check_sheet})




