from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^newsdetail/comment/add/(?P<pk>\d+)/$', views.add_comment, name='add_comment'),
    url(r'^panel/newsdetail/comment/list/$', views.comments_list, name='comments_list'),
    url(r'^panel/newsdetail/comment/del/(?P<pk>\d+)/$', views.comment_delete, name='comment_delete'),
    url(r'^panel/newsdetail/comment/publish/(?P<pk>\d+)/$', views.comment_publish, name='comment_publish'),

]
