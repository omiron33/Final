from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^/registration$', views.reg),
    url(r'^/login$', views.login),
    url(r'^/success$', views.success)
]