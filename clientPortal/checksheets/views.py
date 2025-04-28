# checksheets/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Checksheet
from .forms import ChecksheetForm

@login_required
def create_checksheet(request):
    if request.user.is_nris or request.user.is_superuser:
        if request.method == 'POST':
            form = ChecksheetForm(request.POST)
            if form.is_valid():
                checksheet = form.save(commit=False)
                checksheet.created_by = request.user
                checksheet.save()
                return redirect('nris_dashboard')
        else:
            form = ChecksheetForm()
        return render(request, 'nris/create_checksheet.html', {'form': form})
    else:
        return redirect('admin_dashboard')
