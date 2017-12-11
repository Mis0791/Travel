from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    return render(request, 'login/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/') 

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/travel') # redirects to second app

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    return render(request, 'travel/index.html', { "user": User.objects.get(id=request.session['user_id'])})

