from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError

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


# live streaming video
from django.http.response import StreamingHttpResponse
from django.views.decorators import gzip

# import opencv and threading
import cv2
import threading


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
@gzip.gzip_page
def dashboard(request):
    # try:
    #     cam = VideoCamera()
    #     return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    # except:
    #     pass
    # context = {
    #     'title': 'Dashboard',
    #     'active_dashboard': 'active'
    # }
    return render(request, 'dashboard.html')



# @login_required(login_url='user_login')
# class to capture video class from camera opencv
class VideoCamera(object):
    def  __init__(self) :
        # instalasi camera opencv
        self.video = cv2.VideoCapture(1)
        # pengambilan frame
        (self.grabbed, self.frame) = self.video.read()
        # thread untuk update frame
        threading.Thread(target=self.update, args=()).start()

    
    def __del__(self):
        # penghentian pengambilan frame
        self.video.release()

    def get_frame(self):
        # pengambilan frame atau capture frame
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)

        # pengambilan frame dalam bentuk byte
        return jpeg.tobytes()

    def update(self):
        # looping untuk pengambilan frame
        while True:
            # pengambilan frame
            (self.grabbed, self.frame) = self.video.read()
        

def gen(camera):
    # looping untuk pengambilan frame
    while True:
        # pengambilan frame
        frame = camera.get_frame()
        # yield frame
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

# video streaming
@login_required(login_url='user_login')
def video_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e)
        return HttpResponseServerError("Internal server error")