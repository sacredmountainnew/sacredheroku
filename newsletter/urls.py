from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^newsletter/$', views.news_letter, name='news_letter'),
    url(r'^panel/newsletter/email/$', views.news_email, name='news_email'),
    url(r'^panel/newsletter/phone/$', views.news_phone, name='news_phone'),
    url(r'^panel/newsletter/del/(?P<pk>\d+)/$', views.newsletter_delete, name='newsletter_delete'),
]