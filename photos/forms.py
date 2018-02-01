from __future__ import unicode_literals

from django import forms


class AlbumForm(forms.Form):
    
    albumTitle = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'album-title album-title-form', 
        'autocomplete':'off', 
        'placeholder':'album title...'}),
        max_length=120)
                              
    albumImage = forms.FileField()
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'album-date-form', 'placeholder': 'date as: "YYYY-MM-DD"'}))
    # possibly change this into a calendar picker like the admin has. 
    
    photos = forms.fields.FileField(widget=forms.ClearableFileInput(attrs={'class': 'photo-upload-form','multiple':True}))
    
    
