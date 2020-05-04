from django.shortcuts import render, get_list_or_404, redirect
from .models import BlackList
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
import random
from random import randint
#Import current user
from django.contrib.auth.models import User, Group, Permission
from usermanager.models import UserManager
import re
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity

# Create your views here.

def black_list(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    perm = 0
    #"request.user" means current logged User
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error': error})


    blacklist = BlackList.objects.all()

    return render(request, 'back/blacklist.html', {'blacklist':blacklist})

def ip_black_list_add(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    perm = 0
    #"request.user" means current logged User
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error': error})


    if request.method == 'POST':
        ip = request.POST.get('ip')

        bl = BlackList(ip=ip)
        bl.save()
    
    return redirect('black_list')

def ip_black_list_del(request, pk):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    perm = 0
    #"request.user" means current logged User
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error': error})

    
    bl = BlackList.objects.get(pk=pk)
    bl.delete()
    
    return redirect('black_list')