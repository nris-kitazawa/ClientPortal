# check_sheet/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from .forms import *
from .models import *
from core.functions.userCheckHelper import is_guest_user
from core.functions.decorator import guest_forbidden
import random
import string

@guest_forbidden
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

@guest_forbidden
def create_check_sheet(request):
    if request.method == 'POST':
        form = CheckSheetForm(request.POST)
        if form.is_valid():
            # チェックシートを保存
            check_sheet = form.save(commit=False)
            check_sheet.created_by = request.user
            check_sheet.save()

            # ゲストユーザーの発行
            guest_username = check_sheet.id
            guest_password = check_sheet.password
            guest_user = User.objects.create_user(
                username=guest_username,
                password=guest_password,
                is_active=True,
            )
            # ゲストグループに追加
            guest_group, _ = Group.objects.get_or_create(name="guest")
            guest_user.groups.add(guest_group)
            guest_user.save()

            # ゲスト用リンクとパスワードを表示するページに遷移
            return render(request, 'check_sheet_created.html', {
                'check_sheet': check_sheet
            })
    else:
        form = CheckSheetForm()

    return render(request, 'create_check_sheet.html', {'form': form})

@guest_forbidden
def delete_check_sheet(request, id):
    check_sheet = get_object_or_404(CheckSheet, id=id, user=request.user)
    check_sheet.delete()
    return redirect('check_sheet:index')

def check_sheet_detail(request, id):
    if is_guest_user(request.user) and request.user.username != id:
        return HttpResponseForbidden("このページは対応するNRIS社員またはゲストユーザーのみがアクセスできます。")

    check_sheet = get_object_or_404(CheckSheet, id=id)
    form = CheckSheetDetailForm(instance=check_sheet)
    return render(request, "check_sheet_detail.html", {"form" : form, "check_sheet": check_sheet})

def edit_check_sheet(request, id):
    if is_guest_user(request.user) and request.user.username != id:
        return HttpResponseForbidden("このページは対応するNRIS社員またはゲストユーザーのみがアクセスできます。")
    
    check_sheet = get_object_or_404(CheckSheet, id=id)
    system_summary, _ = SystemSummary.objects.get_or_create(check_sheet=check_sheet)
    
    AssessTargetFormSet = modelformset_factory(
        AssessTarget,
        form=AssessTargetForm,
        extra=1,
        can_delete=True
    )
    LoginCredentialFormSet = modelformset_factory(
        LoginCredential,
        form=LoginCredentialForm,
        extra=1,
        can_delete=True
    )
    
    if request.method == "POST":
        formset = AssessTargetFormSet(request.POST, queryset=AssessTarget.objects.filter(check_sheet=check_sheet), prefix="assess_target")
        login_formset = LoginCredentialFormSet(request.POST, queryset=LoginCredential.objects.filter(check_sheet=check_sheet), prefix="login_credential")
        
        if formset.is_valid() and login_formset.is_valid():
            formset.save()
            login_formset.save()
            return redirect("check_sheet:detail", id=check_sheet.id)
    else:
        formset = AssessTargetFormSet(queryset=AssessTarget.objects.filter(check_sheet=check_sheet), prefix="assess_target")
        login_formset = LoginCredentialFormSet(queryset=LoginCredential.objects.filter(check_sheet=check_sheet), prefix="login_credential")

    return render(request, "edit_check_sheet.html", {
        "formset": formset,
        "login_formset": login_formset,
        "check_sheet": check_sheet,
    })
