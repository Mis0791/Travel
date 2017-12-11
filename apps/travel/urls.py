from django.conf.urls import url
from .import views 

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^new$', views.new),
    url(r'^create$', views.create),
    url(r'^view/(?P<number>\d+)$', views.view),
    url(r'^join/(?P<number>\d+)$', views.join),
    url(r'^remove/(?P<number>\d+)$', views.remove),
    url(r'^delete/(?P<number>\d+)$', views.delete),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
]