
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html',{'posts': posts})

def post(request,pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'post.html',{'posts': posts})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Tài khoản đã tồn tại')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email đã tồn tại')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email,password=password)
                user.save

                user_login = auth.authenticate(username=username,password=password2)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.warning(request,'Mật khẩu không khớp')
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_login = auth.authenticate(username=username, password=password)

        if user_login is not None:
            auth.login(request, user_login)
            return redirect('/')
        else:
            messages.warning(request, 'Tài khoản không hợp lệ')
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return render(request,'login.html')