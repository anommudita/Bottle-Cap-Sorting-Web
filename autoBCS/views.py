from django.shortcuts import render, redirect
from django.http import HttpResponse

# message flash django
from django.contrib import messages

# django login dibutuhkan
from django.contrib.auth.decorators import login_required
# django email verify
from django.contrib.auth import login, authenticate
# import model user django
from django.contrib.auth.models import User

from django.contrib.auth import logout as auth_logout

import time


# Create your views here.
def user_login(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            
            # Lakukan proses otentikasi
            user = authenticate(request, username=username, password=password)
            # print(user)
            
            if user is not None:
                        login(request, user)  # Melakukan login
                        return redirect('dashboard')
            else:
                messages.error(request, "Akun belum terdaftar atau password salah!")
                return redirect('user_login')
        
    return render(request, 'login.html')  # Menampilkan halaman login jika bukan metode POST


def user_logout(request):
    # jika tidak ada session di browser
    if not request.user.is_authenticated:
        # return redirect('error_connection')
        print("tidak ada session di browser")
    # menghapus session di browser
    auth_logout(request)
    time.sleep(1.5)

    messages.success(request, "Anda telah berhasil logout")
    return redirect('user_login')


@login_required(login_url='user_login')
def dashboard(request):
    context = {
        'title': 'Dashboard',
        'active_dashboard': 'active'
    }
    return render(request, 'dashboard.html', context)