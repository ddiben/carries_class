
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.homepage, name='home'),
        url(r'^login/$', views.verifyUser, name='login'),
        url(r'^links/$', views.links, name='links')
    ]