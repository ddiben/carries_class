from __future__ import unicode_literals

from django import forms
from .models import MonthlyPosts, Links

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
        
        # She doesn't need to be able to select a previous post, but we'll save them anyway so that I can go in and bring up old ones through the admin.  
        
        
"""  make the link have a click-able title (that is the link), with a description (or maybe with a button that is the link), and a thumbnail preview
    of the link's main page """
    
class LinkEditForm(forms.ModelForm):
    
    class Meta:
        model = Links
        
        widgets = {
            'title': forms.TextInput(attrs= {'class': 'link-title', 'id': 'link-title-form', 'autocomplete': 'off'}),
            'url': forms.TextInput(),
            'description': forms.Textarea(attrs= {'class': 'link-description', 'id': 'link-description-form', 'autocomplete': 'off'})
        }
        fields = ('title', 'description', 'url')