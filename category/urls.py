from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^panel/category/list/$', views.cat_list, name='cat_list'),
    url(r'^panel/category/add/$', views.cat_add, name='cat_add'),
    url(r'^panel/category/export/csv/$', views.cat_export_csv, name='cat_export_csv'),
    url(r'^panel/category/import/csv/$', views.import_cat_csv, name='import_cat_csv'),

]
