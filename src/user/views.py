from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
import hashlib

def register(request):
    status = request.GET.get('status')
    return render(request, 'register.html', {'status':status})

def sigin(request):
    return render(request, 'sigin.html')


def check_register(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    telephone = request.POST.get('telephone')
    
    user = User.objects.filter(email = email)

    if len(user) > 0:
        return redirect('/auth/register/?status=1')
    
    if len(name.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/register/?status=2')
    
    if len(password) < 8:
        return redirect('/auth/register/?status=3')
    
    try:
        password = hashlib.sha256(password.encode()).hexdigest()
        user = User(name = name,
                       email = email,
                       password = password,
                       telephone = telephone)
        user.save()
        return redirect('/auth/register/?status=0')
    except:
        return redirect('/auth/register/?status=4')
