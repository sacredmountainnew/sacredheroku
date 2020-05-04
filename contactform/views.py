from django.shortcuts import render, get_list_or_404, redirect
from .models import ContactForm
from main.models import Main
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
import datetime
# Create your views here.

def contact_add(request):

    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-newsview')
    popnews2 = News.objects.all().order_by('-newsview')[:3]

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
   

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('msg')

        if name == "" or email == "" or message == "":
            msg = "All Fields Required!!!"
            return render(request, 'front/msgbox.html', {'msg':msg, 'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews':popnews, 'popnews2': popnews2})

        ConForm = ContactForm(name=name, email=email, message=message, date=today, time=time)
        ConForm.save()

        msg = "Your Message Received Successfully!!!"
        return render(request, 'front/msgbox.html', {'msg':msg, 'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews':popnews, 'popnews2': popnews2})


    return render(request, 'front/msgbox.html')


def contact_form(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end


    con = ContactForm.objects.all()

    return render(request, 'back/contact_form.html', {'con':con})

def contact_del(request, pk):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end


    con = ContactForm.objects.filter(pk=pk)
    con.delete()

    return redirect('contact_form')
