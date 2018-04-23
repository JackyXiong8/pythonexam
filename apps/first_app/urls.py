from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),   # This line has changed! Notice that urlpatterns is a list, the comma is in
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'dashboard$', views.success),
    url(r'wish_items/create$', views.create),
    url(r'render$', views.createrender),
    url(r'^wish_items/(?P<itemid>\d+)$', views.show),
    url(r'^delete/(?P<itemid>\d+)$', views.delete),
    url(r'^remove/(?P<itemid>\d+)$', views.remove),
    url(r'^add/(?P<itemid>\d+)$', views.add),
]  