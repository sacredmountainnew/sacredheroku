from django.shortcuts import render, get_list_or_404, redirect
from .models import Comment
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
import random
from random import randint
import datetime
#Import current user
from django.contrib.auth.models import User, Group, Permission
from usermanager.models import UserManager
import re



def add_comment(request, pk):

    
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)
    
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    if len(str(minute)) == 1:
        minute = "0" + str(minute)

    today = str(day) + "/" + str(month) + "/" + str(year)
    time = str(hour) + ":" + str(minute)

    newsname = News.objects.get(pk=pk).name

    if request.method == 'POST':

        comment = request.POST.get('msg')
        email = request.POST.get('email')
        name = request.POST.get('name')

    if request.user.is_authenticated:

        manager = UserManager.objects.get(username=request.user)
        comment = Comment(name=manager.name, email=manager.email, comment=comment, date=today, time=time, news_pk=pk)
        comment.save()

    elif not request.user.is_authenticated:

        comment = Comment(name=name, email=email, comment=comment, date=today, time=time, news_pk=pk)
        comment.save()
        
    return redirect('news_detail', word=newsname)

def comments_list(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    perm = 0
    #"request.user" means current logged User
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    #Preventing other users to delete another users news
    if perm == 0:
        newswr = News.objects.get(pk=pk).writer
        if str(newswr) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html',{'error': error})

    comment = Comment.objects.all()

    return render(request, 'back/comment_list.html', {'comment':comment})

def comment_delete(request, pk):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    perm = 0
    #"request.user" means current logged User
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    #Preventing other users to delete another users news
    if perm == 0:
        newswr = News.objects.get(pk=pk).writer
        if str(newswr) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html',{'error': error})
    
    comment = Comment.objects.get(pk=pk)
    comment.delete()

    return redirect('comments_list')

def comment_publish(request, pk):

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
    

    comment = Comment.objects.get(pk=pk)

    #This code is for publishing
    if comment.status == 0:

        comment.status = 1
        comment.save()
    #This code is for unpublishing
    elif comment.status == 1:

        comment.status = 0
        comment.save()
        
    return redirect('comments_list') 


