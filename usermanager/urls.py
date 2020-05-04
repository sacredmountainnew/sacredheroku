from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^panel/user/manager/$', views.user_manager_list, name='user_manager_list'),
    url(r'^panel/user/manager/del/(?P<pk>\d+)/$', views.user_delete, name='user_delete'),
    url(r'^panel/manage/group/$', views.manage_group, name='manage_group'),
    url(r'^panel/manage/group/add/$', views.manage_group_add, name='manage_group_add'),
    url(r'^panel/manage/group/del/(?P<word>.*)/$', views.manage_group_del, name='manage_group_del'),
    url(r'^panel/user/group/(?P<pk>\d+)/$', views.users_group, name='users_group'),
    url(r'^panel/user/add/group/(?P<pk>\d+)/$', views.add_user_togroup, name='add_user_togroup'),
    url(r'^panel/user/group/del/(?P<pk>\d+)/(?P<name>.*)/$', views.group_delete, name='group_delete'),
    url(r'^panel/manage/permission/$', views.manage_permission, name='manage_permission'),
    url(r'^panel/manage/permission/del/(?P<word>.*)/$', views.manage_permission_del, name='manage_permission_del'),
    url(r'^panel/manage/permission/add/$', views.add_permission, name='add_permission'),
    url(r'^panel/user/permission/(?P<pk>\d+)/$', views.users_perm, name='users_perm'),
    url(r'^panel/user/permission/del/(?P<pk>\d+)/(?P<word>.*)/$', views.users_permission_del, name='users_permission_del'),
    url(r'^panel/user/add/permission/(?P<pk>\d+)/$', views.add_user_perm, name='add_user_perm'),
    url(r'^panel/manage/group/permission/(?P<pk>\d+)/$', views.group_perm, name='group_perm'),
    url(r'^panel/manage/group/permission/del/(?P<pk>\d+)/(?P<name>.*)/$', views.group_permission_del, name='group_permission_del'),
    url(r'^panel/manage/group/permission/add/(?P<pk>\d+)/$', views.add_group_perm, name='add_group_perm'),
]