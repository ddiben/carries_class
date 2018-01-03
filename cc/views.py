# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import MonthlyPosts, Links
from .forms import LoginForm, LoginAgainForm

@login_required
def homepage(request):
    return render(request,'cc/homepage.html', {})

def loginagain(request):
    return render(request, 'cc/loginagain.html')

def verifyUser(request):
    secondattempt = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            key =  form.cleaned_data['password_field']
            
            if key=='parentpassword':
                user = authenticate(request, username='parent', password=key)
                login(request, user)
                return HttpResponseRedirect('/home/')
            
            elif key=='carriespassword':
                user = authenticate(request, username='carrieUser', password=key)
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                secondattempt = True
    
    if secondattempt == True:
        form = LoginAgainForm()
    else:
        form = LoginForm()
    
    return render(request, 'cc/login.html', {'form': form})
