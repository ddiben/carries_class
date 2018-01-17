from __future__ import unicode_literals

from django import forms
from .models import MonthlyPosts

class LoginForm(forms.Form):
    password_field = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'login-input'}), label="", max_length=100)

class LoginAgainForm(forms.Form):
    password_field = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'login-input', 'placeholder' : 'incorrect key'}), label="", max_length=100)
    
class PostEditForm(forms.ModelForm):
    
    class Meta:
        model = MonthlyPosts
        try:
            post =  MonthlyPosts.objects.get(to_display=True)
        except:
            post = MonthlyPosts.objects.create(title="No post to display", text="Looks like there\'s nothing going on")
            post.set_post_to_display()
            post.save();
        
        widgets = {
            'title': forms.TextInput(attrs= {'class': 'monthly-header', 'id': 'monthly-header-form', 'autocomplete': 'off'}), 
            'text': forms.Textarea(attrs= {'class': 'monthly-text', 'id': 'monthly-text-form', 'autocomplete': 'off'}) 
        }
        fields = ('title', 'text',)
        
        """ She doesn't ever want to select a previous post, but we want to store them for the year in case we need to access them through the django admin
        so right now I am thinking that we have two buttons: 'save' which allows editing of the current model; and 'new' which stores the final version of
        the previous model, and creates a new post [and new MonthlyPost object]. """