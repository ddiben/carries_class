# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, LoginAgainForm

@login_required(redirect_field_name=None) # 'redirect_field_name' removes the '?next=' from the url after redirection
def homepage(request, expTime=360):
    request.session.set_expiry(expTime)
    return render(request,'cc/homepage.html', {})

def verifyUser(request):
    secondattempt = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            key =  form.cleaned_data['password_field']
            
            if key=='parentpassword':
                user = authenticate(request, username='parent', password=key)
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            
            elif key=='carriespassword':
                user = authenticate(request, username='carrieUser', password=key)
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                secondattempt = True
    
    if secondattempt == True:
        form = LoginAgainForm()
    else:
        form = LoginForm()
    
    return render(request, 'cc/login.html', {'form': form})
