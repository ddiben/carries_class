from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^photos/$', views.photospage, name='photos'),
        url(r'^photos/(?P<slug>[-\w]+)$', views.albumView , name='album'),
        url(r'^photos/new-album/', views.new_albumView, name='new_album')
    ]