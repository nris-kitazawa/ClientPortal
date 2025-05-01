# check_sheet/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CheckSheetForm
from .models import CheckSheet
import random
import string

def create_check_sheet(request):
    if request.method == 'POST':
        form = CheckSheetForm(request.POST)
        if form.is_valid():
            # チェックシートを保存
            check_sheet = form.save(commit=False)
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
from django.shortcuts import render, get_object_or_404, redirect
from .models import CheckSheet

def delete_check_sheet(request, id):
    check_sheet = get_object_or_404(CheckSheet, id=id, user=request.user)
    check_sheet.delete()
    return redirect('check_sheet:index')

from django.shortcuts import render, redirect, get_object_or_404
from .models import CheckSheet
from .forms import CheckSheetForm, CheckSheetDetailForm
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

def check_sheet_detail(request, id):
    check_sheet = get_object_or_404(CheckSheet, id=id)
    form = CheckSheetDetailForm(instance=check_sheet)
    return render(request, "check_sheet_detail.html", {"form" : form, "check_sheet": check_sheet})

from .forms import CheckSheetEditForm
from django.shortcuts import redirect

def edit_check_sheet(request, id):
    check_sheet = get_object_or_404(CheckSheet, id=id, created_by=request.user)

    if request.method == "POST":
        form = CheckSheetEditForm(request.POST, instance=check_sheet)
        if form.is_valid():
            form.save()
            return redirect("check_sheet:detail", id=check_sheet.id)
    else:
        form = CheckSheetEditForm(instance=check_sheet)

    return render(request, "edit_check_sheet.html", {"form": form, "check_sheet": check_sheet})

def guest_check_sheet_detail(request, uuid):
    check_sheet = get_object_or_404(CheckSheet, uuid=uuid)
    return render(request, 'check_sheet_detail', {
        'check_sheet': check_sheet
    })



