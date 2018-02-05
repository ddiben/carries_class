
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.homepage, name='home'),
        url(r'^login/$', views.verifyUser, name='login'),
        url(r'^links', views.links, name='links'),
        url(r'^math', views.content_not_ready, name="math"),
        url(r'^bio', views.content_not_ready, name="bio"),
        url(r'^parents', views.content_not_ready, name="parents"),
    ]