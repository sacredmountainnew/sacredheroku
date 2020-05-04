from django.shortcuts import render, get_list_or_404, redirect
from .models import Trending
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def trending_add(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    if request.method == 'POST':

        text = request.POST.get('txt')

        if text == "":
            error = "Please Add Trending News"
            return render(request, 'back/error.html',{'error': error})

        trend = Trending(text=text)
        trend.save()

    trendlist = Trending.objects.all()

    return render(request, 'back/trending.html', {'trendlist':trendlist})

def trending_del(request, pk):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    trend = Trending.objects.filter(pk=pk)
    trend.delete()

    return redirect('trending_add')

def trending_edit(request, pk):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    trend = Trending.objects.get(pk=pk)

    if request.method == 'POST':

        text = request.POST.get('txt')

        if text == "":
            error = "Please Add Trending News"
            return render(request, 'back/error.html',{'error': error})

        t = Trending.objects.get(pk=pk)
        t.text = text
        t.save()
        return redirect('trending_add')

    return render(request, 'back/trending_edit.html', {'pk':pk, 'trend':trend})


    
