
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Album, Photo
from .forms import AlbumForm

from django.http.response import HttpResponseRedirect

from cc3site.settings import MEDIAFILES_LOCATION as MEDIA_ROOT #bucket compatibility
import os
import subprocess

from django.core.cache import cache

@login_required(redirect_field_name=None)
def photospage(request):       
    
    if request.method == "POST":
        if request.POST['delete']:
            if request.POST['slug']:
                try:
                    Album.objects.get(slug=request.POST['slug']).delete()
                    
                    cleanup_media = "python3 manage.py cleanup_unused_media -e images/* -e .DS_Store --noinput"
                    cmd_list = cleanup_media.split()
                    cleaning = subprocess.Popen(cmd_list)
                    cleaning.wait()
                    #cleanupDirs("CACHE") - this is only necessary when not in debug mode
                    cache.clear() 
                    
                except:
                    print("Unable to delete album with slug: {}".format(request.POST['slug']))
            
    albums = Album.objects.all().order_by('-date')
    
    return render(request, 'photos/photospage.html', {'albums': albums})
    

def cleanupDirs(dir_name):
    """ Recursively removes empty directories from the file system """
    for dirname, subdirList, fileList in os.walk(os.path.join(MEDIA_ROOT, dir_name), topdown=False):
        print(dirname, subdirList, fileList)
        for directory in subdirList:
            try:
                os.rmdir("{}/{}".format(dirname,directory))
                print("Removed: {}".format(directory))
            except:
                print("Unable to remove: {}".format(directory))
    
@login_required(redirect_field_name=None)
def albumView(request, slug):
    selected_album = Album.objects.get(slug=slug)
    photos = selected_album.photo_set.all()
    
    return render(request, 'photos/album_view.html', {'photos': photos})

@login_required(redirect_field_name=None)
def new_albumView(request):
    if request.user.username == 'parent':
        return HttpResponseRedirect(reverse('photos')) # they can't really get here, but just in case
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_images = request.FILES.getlist('photos')
            
            new_album = Album.objects.create(
                title=form.cleaned_data['albumTitle'],
                image=form.cleaned_data['albumImage'],
                date = form.cleaned_data['date']
                )
            for image in uploaded_images:
                Photo.objects.create(
                    image=image,
                    album=new_album
                    )
            
            return HttpResponseRedirect(reverse('photos'))    
    
    form = AlbumForm()
    
    return render(request, 'photos/new_album_view.html', {'form': form})
