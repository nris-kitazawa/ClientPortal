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
    required_question, _ = RequiredQuestion.objects.get_or_create(check_sheet=check_sheet)
    prepared_docs, _ = PreparedDocs.objects.get_or_create(check_sheet=check_sheet)
    assess_schedule, _ = AssessSchedule.objects.get_or_create(check_sheet=check_sheet)

    # --- フォームとフォームセットの定義をまとめる ---
    form_configs = [
        {
            "type": "form",
            "name": "check_sheet_form",
            "form_class": CheckSheetEditForm,
            "instance": check_sheet,
        },
        {
            "type": "form",
            "name": "system_summary_form",
            "form_class": SystemSummaryForm,
            "instance": system_summary,
        },
        {
            "type": "formset",
            "name": "formset",
            "formset_class": modelformset_factory(
                AssessTarget, form=AssessTargetForm, extra=1 if AssessTarget.objects.filter(check_sheet=check_sheet).count() == 0 else 0,  # extra を動的に設定, can_delete=True
            ),
            "queryset": AssessTarget.objects.filter(check_sheet=check_sheet),
            "prefix": "assess_target",
            "assign_check_sheet": True,
        },
        {
            "type": "formset",
            "name": "login_formset",
            "formset_class": modelformset_factory(
                LoginCredential, form=LoginCredentialForm, extra=1 if LoginCredential.objects.filter(check_sheet=check_sheet).count() == 0 else 0, can_delete=True
            ),
            "queryset": LoginCredential.objects.filter(check_sheet=check_sheet),
            "prefix": "login_credential",
            "assign_check_sheet": True,
        },
        {
            "type" : "form",
            "name" : "required_question_form",
            "form_class" : RequiredQuestionForm,
            "instance" : required_question,
        },
        {
            "type": "form",
            "name": "prepared_docs_form",
            "form_class": PreparedDocsForm,
            "instance": prepared_docs,
        },
        {
            "type": "form",
            "name": "assess_schedule_form",
            "form_class": AssessScheduleForm,
            "instance": assess_schedule,
        },
        {
            "type": "formset",
            "name": "member_formset",
            "formset_class": modelformset_factory(
                Member, form=MemberForm, extra=1 if Member.objects.filter(check_sheet=check_sheet).count() == 0 else 0, can_delete=True
            ),
            "queryset": Member.objects.filter(check_sheet=check_sheet),
            "prefix": "member",
            "assign_check_sheet": True,
        },
    ]

    context = {"check_sheet": check_sheet}

    if request.method == "POST":
        all_valid = True

        for config in form_configs:
            if config["type"] == "form":
                form = config["form_class"](request.POST, instance=config["instance"])
                context[config["name"]] = form
                if not form.is_valid():
                    all_valid = False

            elif config["type"] == "formset":
                formset = config["formset_class"](
                    request.POST,
                    queryset=config["queryset"],
                    prefix=config["prefix"]
                )
                context[config["name"]] = formset
                if not formset.is_valid():
                    all_valid = False

        if all_valid:
            for config in form_configs:
                if config["type"] == "form":
                    context[config["name"]].save()
                elif config["type"] == "formset":
                    instances = context[config["name"]].save(commit=False)

                    for obj in instances:
                        print(config["name"], obj)
                        if config.get("assign_check_sheet"):
                            obj.check_sheet = check_sheet
                        obj.save()
                    for obj in context[config["name"]].deleted_objects:
                        obj.delete()

            return redirect("check_sheet:detail", id=check_sheet.id)

    else:
        for config in form_configs:
            if config["type"] == "form":
                context[config["name"]] = config["form_class"](instance=config["instance"])
            elif config["type"] == "formset":
                context[config["name"]] = config["formset_class"](
                    queryset=config["queryset"],
                    prefix=config["prefix"]
                )

    return render(request, "edit_check_sheet.html", context)