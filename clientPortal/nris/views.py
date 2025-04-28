# checksheets/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def nris_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_nris:
            login(request, user)
            return redirect('nris_dashboard')
        else:
            return render(request, 'nris/login.html', {'error': 'Invalid credentials or not an NRIS user'})
    return render(request, 'nris/login.html')

@login_required
def nris_dashboard(request):
    if request.user.is_nris:
        return render(request, 'nris/dashboard.html')
    else:
        return redirect('admin_dashboard')
