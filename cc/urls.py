
from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
        url(r'^$', views.verifyUser, name='rootlogin'),
        url(r'^login/$', views.verifyUser),
        url(r'^loginagain/$', views.loginagain),
        url(r'^home/$', views.homepage),
        url(r'.*$', RedirectView.as_view(pattern_name='rootlogin', permanent=False)),
    ]