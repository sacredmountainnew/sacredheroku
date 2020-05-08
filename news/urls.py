from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^news/(?P<word>.*)/$', views.news_detail, name='news_detail'),
    url(r'^panel/news/list/$', views.news_list, name='news_list'),
    url(r'^panel/news/add/$', views.news_add, name='news_add'),
    url(r'^panel/news/list/del/(?P<pk>\d+)/$', views.news_delete, name='news_delete'),
    url(r'^panel/news/edit/(?P<pk>\d+)/$', views.news_edit, name='news_edit'),
    url(r'^panel/news/publish/(?P<pk>\d+)/$', views.news_publish, name='news_publish'),
    url(r'^urls/(?P<rand>\d+)/$', views.news_detail_short, name='news_detail_short'),
    url(r'^show/all/news/(?P<word>.*)/$', views.show_all_news, name='show_all_news'),
    url(r'^all/news/$', views.all_news, name='all_news'),
    url(r'^search/$', views.all_news_search, name='all_news_search'),


]
