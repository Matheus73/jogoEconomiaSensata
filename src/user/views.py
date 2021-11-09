from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
import hashlib


def register(request):
    if request.session.get('user'):
        return redirect('/')
    status = request.GET.get('status')
    return render(request, 'register.html', {'status': status})


def signin(request):
    if request.session.get('user'):
        return redirect('/')
    status = request.GET.get('status')
    return render(request, 'signin.html', {'status': status})


def check_register(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    telephone = request.POST.get('telephone')

    user = User.objects.filter(email=email)

    if len(user) > 0:
        return redirect('/auth/register/?status=1')

    if len(name.strip()) == 0 or len(email.strip()) == 0 or len(telephone.strip()) == 0:
        return redirect('/auth/register/?status=2')

    if len(password) < 8:
        return redirect('/auth/register/?status=3')

    try:
        password = hashlib.sha256(password.encode()).hexdigest()
        user = User(name=name,
                    email=email,
                    password=password,
                    telephone=telephone)
        user.save()
        request.session['user'] = user.id
        return redirect('/')
    except:
        return redirect('/auth/register/?status=4')


def check_signin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password = hashlib.sha256(password.encode()).hexdigest()
    users = User.objects.filter(email=email).filter(password=password)

    if len(users) == 0:
        return redirect('/auth/signin/?status=1')
    elif len(users) > 0:
        request.session['user'] = users[0].id
        return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/auth/signin/')
