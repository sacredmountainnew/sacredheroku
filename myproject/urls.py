"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

#For XML Page
from django.contrib.sitemaps.views import sitemap
from main.sitemap import MyNewsSiteMap

#For Rest Frame Work
from rest_framework import routers
from main import views

router = routers.DefaultRouter()
router.register(r'mynews', views.NewsViewSet)


sitemaps = {

    'news': MyNewsSiteMap(),
}

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),

    #For Rest Frame Work
    url(r'rest/', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #For XML Page
    url(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


    #For collectstatic files
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),

    url(r'', include('main.urls')),
    url(r'', include('news.urls')),
    url(r'', include('category.urls')),
    url(r'', include('subcategory.urls')),
    url(r'', include('contactform.urls')),
    url(r'', include('trending.urls')),
    url(r'', include('usermanager.urls')),
    url(r'', include('newsletter.urls')),
    url(r'', include('comment.urls')),
    url(r'', include('blacklist.urls')),
] 

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



