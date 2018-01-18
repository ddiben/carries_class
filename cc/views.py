# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, LoginAgainForm, PostEditForm, LinkEditForm

from .models import MonthlyPosts, Links

@login_required(redirect_field_name=None) # 'redirect_field_name' removes the '?next=' from the url after redirection
def homepage(request, expTime=9000):
    request.session.set_expiry(expTime)
    
    try:
        postToDisplay = MonthlyPosts.objects.get(to_display=True)
    except:
        postToDisplay_if_not = MonthlyPosts.objects.get_or_create(title='No post to display', text='Looks like there isn\'t anything going on')
        postToDisplay = postToDisplay_if_not[0]
        postToDisplay.set_post_to_display()
        postToDisplay.save()
    
    if request.user.username == 'carrieUser':
        if request.method == 'POST':
            form = PostEditForm(request.POST)
            
            if form.is_valid():
                if request.POST.get('save'):
                    postToDisplay.title = form.cleaned_data['title']
                    postToDisplay.text = form.cleaned_data['text']
                    postToDisplay.save()
                if request.POST.get('new'):
                    postToDisplay.title = form.cleaned_data['title']
                    postToDisplay.text = form.cleaned_data['text']
                    postToDisplay.save()
                    
                    postToDisplay_if_not = MonthlyPosts.objects.get_or_create(title="blank title", text="write something new")
                    postToDisplay = postToDisplay_if_not[0]
                    postToDisplay.set_post_to_display()
                    postToDisplay.save()
                
        else:
            form = PostEditForm()
        return render(request, 'cc/homepage.html', {
            'monthly_post': postToDisplay, # this is kept around for testing purposes, the page doesn't render this information exactly
            'form': form, 
            'monthly_post_title_json': json.dumps(postToDisplay.title), 
            'monthly_post_text_json': json.dumps(postToDisplay.text) })
            
    return render(request,'cc/homepage.html', {'monthly_post': postToDisplay})

@login_required(redirect_field_name=None)
def links(request):
    if request.method == 'POST':
        if request.user.username == 'carrieUser':
            
            form = LinkEditForm(request.POST)
            
            if form.is_valid():
                
                Links.objects.create(
                    title=form.cleaned_data['title'], 
                    url=form.cleaned_data['url'], 
                    description=form.cleaned_data['description'])
                
                
            
    
    linksToDisplay = Links.objects.all()
    
    return render(request, 'cc/linkspage.html', {'links': linksToDisplay, 'numLinks': len(linksToDisplay)})

# the login view, but I didin't want to overwrite Django's (because that was more complicated than just calling mine something else). 
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
