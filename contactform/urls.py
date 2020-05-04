from django.conf.urls import url
from . import views

urlpatterns = [

url(r'^contact/submit/$', views.contact_add, name='contact_add'),
url(r'^panel/contact/form/$', views.contact_form, name='contact_form'),
url(r'^panel/contact/form/del/(?P<pk>\d+)/$', views.contact_del, name='contact_del'),
    
]
