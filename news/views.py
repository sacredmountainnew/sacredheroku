from django.shortcuts import render, get_list_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcategory.models import SubCategory
from category.models import Category
from trending.models import Trending
from django.contrib.contenttypes.models import ContentType
import random
from comment.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

# Create your views here.
#Global variable for search(otherways second page from search pagination will not work)
mysearch = ""

def news_detail(request, word):
     
    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()

    lastnews = News.objects.all().order_by('-pk')[:3]

    shownews = News.objects.filter(name=word)

    popnews = News.objects.all().order_by('-newsview')

    popnews2 = News.objects.all().order_by('-newsview')[:3]

    tagname = News.objects.get(name=word).tag
    tag = tagname.split(',')

    trend = Trending.objects.all().order_by('-pk')[:5]

    #Code is for views of page
    try:

        mynews = News.objects.get(name=word)
        mynews.newsview = mynews.newsview + 1
        mynews.save()

    except:

        print("Can\'t Add Show")

    #For QR Code generation
    link = "/urls/" + str(News.objects.get(name=word).rand)

    code = News.objects.get(name=word).pk
    comment = Comment.objects.filter(news_pk=code, status=1).order_by('-pk')[:10]
    cmcount = len(comment)

    return render(request, 'front/news_detail.html', {'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'shownews':shownews, 'popnews':popnews, 'popnews2':popnews2, 'tag':tag, 'trend':trend, 'code':code, 'comment':comment, 'cmcount':cmcount, 'link':link, 'tagname':tagname})

#Shortening the url to random number
def news_detail_short(request, rand):
     
    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()

    lastnews = News.objects.all().order_by('-pk')[:3]

    shownews = News.objects.filter(rand=rand)

    popnews = News.objects.all().order_by('-newsview')

    popnews2 = News.objects.all().order_by('-newsview')[:3]

    tagname = News.objects.get(rand=rand).tag
    tag = tagname.split(',')

    trend = Trending.objects.all().order_by('-pk')[:5]

    #Code is for views of page
    try:

        mynews = News.objects.get(rand=rand)
        mynews.newsview = mynews.newsview + 1
        mynews.save()

    except:

        print("Can\'t Add Show")
    
    #For QR Code generation
    link = "/urls/" + str(News.objects.get(rand=rand).rand)

    code = News.objects.get(rand=rand).pk
    comment = Comment.objects.filter(news_pk=code, status=1).order_by('-pk')[:10]
    cmcount = len(comment)


    return render(request, 'front/news_detail.html', {'site': site, 'news': news, 'cat':cat, 'subcat': subcat, 'lastnews': lastnews, 'shownews':shownews, 'popnews':popnews, 'popnews2':popnews2, 'tag':tag, 'trend':trend, 'code':code, 'comment':comment, 'cmcount':cmcount, 'link':link})



def news_list(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    perm = 0
    #"request.user" means current logged User
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    #If the logged user is a normal user only list their news
    if perm == 0:
        news = News.objects.filter(writer=request.user)

    #If the logged user is admin list all news
    elif perm == 1:
        news = News.objects.all().order_by('-pk')
        #Pagination is preventing all pages loading in a single page
        #Pagination of News List(2 news per page)
        paginator = Paginator(news, 4)

        page = request.GET.get('page')#Here 'page' is class name of table.

        try:
            newspage = paginator.page(page)

        except EmptyPage:
            newspage = paginator.page(paginator, num_page)

        except PageNotAnInteger:
            newspage = paginator.page(1)

    return render(request, 'back/news_list.html', {'newspage': newspage})

def news_add(request):

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

    subcat = SubCategory.objects.all()

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

    date = str(day) + str(month) + str(year)
    
    randint  = str(random.randint(1000, 9999))
    rand = date + randint
    rand = int(rand)

    while (len(News.objects.filter(rand=rand))) != 0:

        randint  = str(random.randint(1000, 9999))
        rand = date + randint
        rand = int(rand)



    if request.method == 'POST':

        newstitle = request.POST.get('newstitle')
        newssubcat = request.POST.get('newssubcat')
        newssum = request.POST.get('newssum')
        newsbody = request.POST.get('newsbody')
        newssubcatid = request.POST.get('newssubcat') 
        tag = request.POST.get('tag')

        if newstitle == "" or newssubcat == "" or newssum == "" or newsbody == "":

            error = "All Fields Required"
            return render(request, 'back/error.html',{'error': error})
        try:

            myfile = request.FILES['imagefile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):  

                if myfile.size < 5000000:

                    newsname = SubCategory.objects.get(pk=newssubcatid).name
                    catid = SubCategory.objects.get(pk=newssubcatid).catid

                    newsModel = News(name=newstitle, short_text=newssum, body_text=newsbody, date=today, time=time, picname=filename, picurl=url, writer=request.user, subcatname=newsname, subcatid=newssubcatid, newsview=1, catid=catid, tag=tag, rand=rand)
                    newsModel.save()

                    
                    count = len(News.objects.filter(catid=catid))
                    catCount = Category.objects.get(pk=catid)
                    catCount.count = count
                    catCount.save()
                    
                    
                    return redirect('news_list')
                else:
                    error = "File Size is bigger than 5MB"
                    return render(request, 'back/error.html',{'error': error})
            
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "File Not supported"
                return render(request, 'back/error.html',{'error': error})
       
        except:

            error = "Please upload image"
            return render(request, 'back/error.html',{'error': error})

    return render(request, 'back/news_add.html', {'subcat':subcat})   

def news_delete(request, pk):
    
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
    

    try:
        newsDel = News.objects.get(pk=pk)

        fs = FileSystemStorage()
        fs.delete(newsDel.picname)

        catid = News.objects.get(pk=pk).catid

        newsDel.delete()

        
        count = len(News.objects.filter(catid=catid))
        catC = Category.objects.get(pk=catid)
        catC.count = count
        catC.save()
        
       
    except:
        error = "Something Wrong"
        return render(request, 'back/error.html',{'error': error})
    
    
    return redirect('news_list')


    

def news_edit(request, pk):

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

  
    

    if len(News.objects.filter(pk=pk)) == 0:
        error = "News not found"
        return render(request, 'back/error.html',{'error': error})

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

    subcat = SubCategory.objects.all()
    news = News.objects.get(pk=pk)
    
    if request.method == 'POST':

        newstitle = request.POST.get('newstitle')
        newssubcat = request.POST.get('newssubcat')
        newssum = request.POST.get('newssum')
        newsbody = request.POST.get('newsbody')
        newsid = request.POST.get('newssubcat') 
        tag = request.POST.get('tag')
        
        if newstitle == "" or newssubcat == "" or newssum == "" or newsbody == "":

            error = "All Fields Required"
            return render(request, 'back/error.html',{'error': error})
        try:

            myfile = request.FILES.get('myfile')
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                
                if myfile.size < 5000000:
                    newsname = SubCategory.objects.get(pk=newsid).name

                    newsModel = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(newsModel.picname)

                    newsModel.name = newstitle
                    newsModel.short_text = newssum
                    newsModel.body_text = newsbody
                    newsModel.picname = filename
                    newsModel.picurl = url
                    newsModel.subcatname = newsname
                    newsModel.subcatid = newsid
                    newsModel.date=today 
                    newsModel.time=time
                    newsModel.tag = tag
                    newsModel.activate = 0
                    newsModel.save()

                    return redirect('news_list')
                else:
                    error = "File Size is bigger than 5MB"
                    return render(request, 'back/error.html',{'error': error})
            
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "File Not supported"
                return render(request, 'back/error.html',{'error': error})
       
        except:
            
            newsname = SubCategory.objects.get(pk=newsid).name

            newsModel = News.objects.get(pk=pk)

            newsModel.name = newstitle
            newsModel.short_text = newssum
            newsModel.body_text = newsbody
            newsModel.subcatname = newsname
            newsModel.subcatid = newsid
            newsModel.date=today 
            newsModel.time=time
            newsModel.tag = tag
            newsModel.activate = 0
            newsModel.save()

            return redirect('news_list')
            

    return render(request, 'back/news_edit.html', {'pk':pk,'news':news, 'subcat':subcat})
    


def news_publish(request, pk):

    '''
    Filtering with activate = 1
-------------------------------------
    def home(request):

    site = Main.objects.get(pk=1)
    news = News.objects.filter(activate=1).order_by('-pk')
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    lastnews = News.objects.filter(activate=1).order_by('-pk')[:3]
    popnews = News.objects.filter(activate=1).order_by('-newsview')
    popnews2 = News.objects.filter(activate=1).order_by('-newsview')[:3]

    '''
    
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
    

    news = News.objects.get(pk=pk)

    #This code is for publishing
    if news.activate == 0:
        news.activate = 1
        news.save()
    #This code is for unpublishing
    elif news.activate == 1:
        news.activate = 0
        news.save()
        
    return redirect('news_list') 

def show_all_news(request, word):

    trend = Trending.objects.all().order_by('-pk')[:5]
    site = Main.objects.get(pk=1)
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    popnews2 = News.objects.filter(activate=1).order_by('-newsview')[:3]
    news = News.objects.filter(activate=1).order_by('-pk')

    catid = Category.objects.get(name=word).pk
    catname = word
    newscat = News.objects.filter(catid=catid)

    return render(request, 'front/all_news.html', {'catname':catname, 'news':news, 'newscat':newscat, 'site':site, 'trend':'trend', 'cat':cat, 'subcat':subcat, 'popnews2':popnews2})


      
def all_news(request):

    trend = Trending.objects.all().order_by('-pk')[:5]
    site = Main.objects.get(pk=1)
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    popnews2 = News.objects.filter(activate=1).order_by('-newsview')[:3]
    newscat = News.objects.filter(activate=1).order_by('-pk')

    f_rom = []
    t_o = []

    for i in range(30):
        #datetime.datetime.now() + datetime.timedelta(days=i)means it will add 1  for range upto 9
        #datetime.datetime.now() - datetime.timedelta(days=i)means it will minus 1 for range upto 9
        now = datetime.datetime.now() - datetime.timedelta(days=i)
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        now = str(day) + "/" + str(month) + "/" + str(year)

        f_rom.append(now)
    
    for i in range(30):
        #datetime.datetime.now() + datetime.timedelta(days=i)means it will add 1  for range upto 9
        #datetime.datetime.now() - datetime.timedelta(days=i)means it will minus 1 for range upto 9
        now = datetime.datetime.now() - datetime.timedelta(days=i)
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        now = str(day) + "/" + str(month) + "/" + str(year)

        t_o.append(now)

    paginator = Paginator(newscat, 12)
    page = request.GET.get('page')#Here 'page' is class name of table.

    try:
        newspage = paginator.page(page)

    except EmptyPage:
        newspage = paginator.page(paginator, num_page)

    except PageNotAnInteger:
        newspage = paginator.page(1)

    return render(request, 'front/showall_news.html', {'newscat':newscat, 'site':site, 'trend':'trend', 'cat':cat, 'subcat':subcat, 'popnews2':popnews2, 'f_rom':f_rom, 't_o':t_o})

def all_news_search(request):

    if request.method == 'POST':

        txt = request.POST.get('txt')
        catid = request.POST.get('cat')
        f_rom = request.POST.get('from')
        t_o = request.POST.get('to')
        mysearch = txt

        if f_rom != "0" and t_o != "0":#means fromdate and to date are selected
            if t_o < f_rom:
                msg = "Date Error!!!"
                return render(request, 'front/msgbox.html', {'msg':msg})

      
        if catid == "0":#For searching in all news
            #For searching category wise
            if f_rom != "0" and t_o != "0":#both from date and to date selected

                query1 = News.objects.filter(activate=1, name__contains=txt, date__gte=f_rom, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, date__gte=f_rom, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, date__gte=f_rom, date__lte=t_o)

            elif f_rom != "0":#only from date selected

                query1 = News.objects.filter(activate=1, name__contains=txt, date__gte=f_rom)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, date__gte=f_rom)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, date__gte=f_rom)
            
            elif t_o != "0":#only to date selected

                query1 = News.objects.filter(activate=1, name__contains=txt, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, date__lte=t_o)
            

            else:#show all news with search

                query1 = News.objects.filter(activate=1, name__contains=txt)
                query2 = News.objects.filter(activate=1, short_text__contains=txt)
                query3 = News.objects.filter(activate=1, body_text__contains=txt)

            
        else:

            if f_rom != "0" and t_o != "0":#both from date and to date selected

                query1 = News.objects.filter(activate=1, name__contains=txt, catid=catid, date__gte=f_rom, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, catid=catid, date__gte=f_rom, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, catid=catid, date__gte=f_rom, date__lte=t_o)
            
            elif f_rom != "0":#only from date selected

                query1 = News.objects.filter(activate=1, name__contains=txt, catid=catid, date__gte=f_rom)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, catid=catid, date__gte=f_rom)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, catid=catid, date__gte=f_rom)
            
            elif t_o != "0":#only to date selected

                query1 = News.objects.filter(activate=1, name__contains=txt, catid=catid, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, catid=catid, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, catid=catid, date__lte=t_o)
            
            else:#show all news with search

                query1 = News.objects.filter(activate=1, name__contains=txt, catid=catid)
                query2 = News.objects.filter(activate=1, short_text__contains=txt, catid=catid)
                query3 = News.objects.filter(activate=1, body_text__contains=txt, catid=catid)

        newscat = list(chain(query1, query2, query3))#To merge all queries(from itertools import chain)
        newscat = list(dict.fromkeys(newscat))#To make a single query(otherways query will repeat 3 times)

    else:

        if catid == "0":#For searching in all news
            #For searching category wise
            
            if f_rom != "0" and t_o != "0":

                query1 = News.objects.filter(activate=1, name__contains=mysearch, date__gte=f_rom, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, date__gte=f_rom, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, date__gte=f_rom, date__lte=t_o)
            
            elif f_rom != "0":

                query1 = News.objects.filter(activate=1, name__contains=mysearch, date__gte=f_rom)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, date__gte=f_rom)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, date__gte=f_rom)
            
            elif t_o != "0":

                query1 = News.objects.filter(activate=1, name__contains=mysearch, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, date__lte=t_o)
            

            else:
                
                query1 = News.objects.filter(activate=1, name__contains=mysearch)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch)
            

        else:

            if f_rom != "0" and t_o != "0":

                query1 = News.objects.filter(activate=1, name__contains=mysearch, catid=catid, date__gte=f_rom, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, catid=catid, date__gte=f_rom, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, catid=catid, date__gte=f_rom, date__lte=t_o)
            
            elif f_rom != "0":

                query1 = News.objects.filter(activate=1, name__contains=mysearch, catid=catid, date__gte=f_rom)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, catid=catid, date__gte=f_rom)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, catid=catid, date__gte=f_rom)
            
            elif t_o != "0":

                query1 = News.objects.filter(activate=1, name__contains=mysearch, catid=catid, date__lte=t_o)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, catid=catid, date__lte=t_o)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, catid=catid, date__lte=t_o)
            
            else:

                query1 = News.objects.filter(activate=1, name__contains=mysearch, catid=catid,)
                query2 = News.objects.filter(activate=1, short_text__contains=mysearch, catid=catid,)
                query3 = News.objects.filter(activate=1, body_text__contains=mysearch, catid=catid,)



        newscat = list(chain(query1, query2, query3))#To merge all queries(from itertools import chain)
        newscat = list(dict.fromkeys(newscat))#To make a single query(otherways query will repeat 3 times)

    trend = Trending.objects.all().order_by('-pk')[:5]
    site = Main.objects.get(pk=1)
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    popnews2 = News.objects.filter(activate=1).order_by('-newsview')[:3]
    
    f_rom = []
    t_o = []

    for i in range(30):

        #datetime.datetime.now() + datetime.timedelta(days=i)means it will add 1  for range upto 9
        #datetime.datetime.now() - datetime.timedelta(days=i)means it will minus 1 for range upto 9
        now = datetime.datetime.now() - datetime.timedelta(days=i)
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
            
        now = str(day) + "/" + str(month) + "/" + str(year)

        f_rom.append(now)
        
    for i in range(30):
        #datetime.datetime.now() + datetime.timedelta(days=i)means it will add 1  for range upto 9
        #datetime.datetime.now() - datetime.timedelta(days=i)means it will minus 1 for range upto 9
        now = datetime.datetime.now() - datetime.timedelta(days=i)
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
            
        now = str(day) + "/" + str(month) + "/" + str(year)

        t_o.append(now)       

   

    paginator = Paginator(newscat, 12)
    page = request.GET.get('page')#Here 'page' is class name of table.

    try:
        newspage = paginator.page(page)

    except EmptyPage:
        newspage = paginator.page(paginator, num_page)

    except PageNotAnInteger:
        newspage = paginator.page(1)
   
    return render(request, 'front/showall_news.html', {'newscat':newscat, 'site':site, 'trend':'trend', 'cat':cat, 'subcat':subcat, 'popnews2':popnews2, 'f_rom':f_rom, 't_o':t_o})

