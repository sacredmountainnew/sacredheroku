from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^panel/ip/blacklist/$', views.black_list, name='black_list'),
    url(r'^panel/ip/blacklist/add/$', views.ip_black_list_add, name='ip_black_list_add'),
    url(r'^panel/ip/blacklist/del/(?P<pk>\d+)/$', views.ip_black_list_del, name='ip_black_list_del'),
    
]
