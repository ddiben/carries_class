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
    
class LinkEditForm(forms.ModelForm):
    
    class Meta:
        model = Links
        
        widgets = {
            'title': forms.TextInput(attrs= {'class': 'link-title link-title-form', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs= {'class': 'link-description link-description-form', 'rows': '5', 'autocomplete': 'off'}),
            'url': forms.URLInput(attrs= {'class': 'link-url link-url-form', 'autocomplete': 'off',  })
            
        }
        fields = ('title', 'description', 'url')
        