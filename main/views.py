from django.shortcuts import render, get_list_or_404, redirect
from .models import Main
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


def home(request):

    site = Main.objects.get(pk=1)
    news = News.objects.filter(activate=1).order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    lastnews = News.objects.filter(activate=1).order_by('-pk')[:3]
    popnews = News.objects.filter(activate=1).order_by('-newsview')
    popnews2 = News.objects.filter(activate=1).order_by('-newsview')[:3]
    trend = Trending.objects.all().order_by('-pk')[:5]
    #For "forloop.counter"
    lastnews2 = News.objects.filter(activate=1).order_by('-pk')[:4]

    #for randomly selecting trending news
    rand_object = Trending.objects.all()[randint(0, len(trend)-1 )]

    return render(request, 'front/home.html', {'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews':popnews, 'popnews2': popnews2, 'trend':trend, 'lastnews2':lastnews2})

def about(request):

    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-newsview')[:3]
    trend = Trending.objects.all().order_by('-pk')[:5]


    return render(request, 'front/about.html', {'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews2': popnews2, 'trend':trend})

def panel(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    #Setting permission to access of side panel in template
    perm = 0
    #Retrieving Permissions of logged user
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.name == "master_user" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error': error})

    return render(request, 'back/home.html')

def my_login(request):
    
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')

        if usern != "" and passw != "":
            user = authenticate(username= usern, password=passw)

            if user != None:
                login(request, user)
                return redirect('panel')


    return render(request, 'front/login.html')

def my_register(request):
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        passverify = request.POST.get('passverify')

        try:

            if name == "":

                msg = "Input Your Name!!"
                return render(request, 'front/msgbox.html', {'msg':msg})

            if password != passverify:

                msg = "Password does not match!!!"
                return render(request, 'front/msgbox.html', {'msg':msg})
            #Checking Password complexity
            if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):

                #Checking whether username or email already exists
                if len(User.objects.filter(username=username)) == 0 and len(User.objects.filter(email=email)) == 0:

                    #For tracing IP of User who registered
                    ip, is_routable = get_client_ip(request)

                    if ip is None:
                        ip = "0.0.0.0"

                    #To find the Geo Location(country and city)
                    try:
                        response = DbIpCity.get(ip, api_key="free")
                        country = response.country + "|" + response.city
                    except:
                        country = "unknown"

                    #Saving credentials
                    user = User.objects.create_user(username=username, email=email, password=password)

                    #For listing registered users in User Manager List || from usermanager.models import UserManager
                    m = UserManager(name=name, username=username, email=email, ip=ip, geolocation=country)
                    m.save() 
                
                else:

                    msg = "Username and Email already exists!!"
                    return render(request, 'front/msgbox.html', {'msg':msg})

            else:

                msg = "Password must have complexity!!"
                return render(request, 'front/msgbox.html', {'msg':msg})
                
        except:
            msg = "Something went wrong!"
            return render(request, 'front/msgbox.html', {'msg':msg})




    return render(request, 'front/login.html')

def my_logout(request):
    
    logout(request)
    return redirect('my_login')

def site_setting(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    if request.method == 'POST':

        name = request.POST.get('name')
        tel = request.POST.get('tel')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')

        if fb == "" : fb = "#"
        if tw == "" : tw = "#"
        if yt == "" : yt = "#"
        if link == "" : link = "#"

        if name == "" or tel == "" or txt == "":
            error = "All Fields Required"
            return render(request, 'back/error.html', {'error': error})
        
        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)
            picurlfoot = url
            picnamefoot = filename

        except:

            picurlfoot = "-"
            picnamefoot = "-"

        try:
            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)
            picurlhead = url2
            picnamehead = filename2
            
        
        except:

            picurlhead = "-"
            picnamehead = "-"

        siteModel = Main.objects.get(pk=1)

        siteModel.name = name
        siteModel.tel = tel
        siteModel.fb = fb
        siteModel.tw = tw
        siteModel.yt = yt
        siteModel.link = link
        siteModel.about = txt

        if picurlfoot != "-": siteModel.picurlfoot = picurlfoot 
        if picnamefoot != "-": siteModel.picnamefoot = picnamefoot
        if picurlhead != "-": siteModel.picurlhead = picurlhead
        if picnamehead != "-": siteModel.picnamehead = picnamehead

        siteModel.save()

        
    site = Main.objects.get(pk=1)

    return render(request, 'back/setting.html', {'site':site})

def about_setting(request):

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
        abouttxt = request.POST.get('txt')

        if abouttxt == "":
            error = "Field Required"
            return render(request, 'back/error.html',{'error': error})
        
        m = Main.objects.get(pk=1)
        m.aboutdetail = abouttxt
        m.save()

    about = Main.objects.get(pk=1).aboutdetail

    return render(request, 'back/about_setting.html', {'about':about})

def contact(request):

    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-newsview')[:3]
    trend = Trending.objects.all().order_by('-pk')[:5]


    return render(request, 'front/contact.html', {'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews2': popnews2, 'trend':trend})

def change_pass(request):


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

        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "":
            error = "All Fields Required"
            return render(request, 'back/error.html',{'error': error})


        #"request.user returns current user"
        user = authenticate(username= request.user, password=oldpass)

        #This line below means user name is correct and old password is correct
        if user != None:

            if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', newpass):

                #<-----from django.contrib.auth.models import User---->
                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('my_logout')

            else:

                error = "Password must contain 8 characters with complexity"
                return render(request, 'back/error.html',{'error': error})

        else:
            error = "Your Old Password is Incorrect"
            return render(request, 'back/error.html',{'error': error})



    return render(request, 'back/change_pass.html')