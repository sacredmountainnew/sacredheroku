from django.shortcuts import render, get_list_or_404, redirect, HttpResponse
from .models import NewsLetter
from django.contrib.auth import authenticate, login, logout
#Import  Users, Group, Permissions
from django.contrib.auth.models import User, Group, Permission
#To add permission to logged user to get which options use / this library very Important
from django.contrib.contenttypes.models import ContentType
#For regex password complexity verification
from django.core.mail import send_mail
from django.conf import settings

def news_letter(request):

    if request.method == 'POST':

        text = request.POST.get('txt')

        #Checking whether the text is Email or Phone Number
        res = text.find('@')

        if int(res) != -1:
            newsl = NewsLetter(text=text, status=1)
            newsl.save()
        else:

            try:
                int(text)

                if len(text) == 10:
                    newsl = NewsLetter(text=text, status=2)
                    newsl.save()
                else:
                    return redirect('home')
            
            except:
                return redirect('home')
       

    return redirect('home')

def news_email(request):

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

    email = NewsLetter.objects.filter(status=1)


    return render(request,'back/email.html', {'email':email})

def news_phone(request):

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

    phone = NewsLetter.objects.filter(status=2)


    return render(request,'back/phone.html', {'phone':phone})

def newsletter_delete(request, pk):

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

    #Deleting newletter with status in single function
    newsl = NewsLetter.objects.get(pk=pk)
    status = newsl.status 
    newsl.delete()

    if status == 1:
        return redirect('news_email')
    elif status == 2:
        return redirect('news_phone')

def send_email(request):

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
        
        text = request.POST.get('text')
        
        emaillist = []
        #Filtering Emails only(status=1 is email, status=2 is phonenumber)
        for i in NewsLetter.objects.filter(status=1):
            emaillist.append(i.text)
        


        subject = 'Reply Mail'
        message = text
        emails = emaillist
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, emails)

    return redirect('news_email')

#To delete checked list
def check_emaillist(request):

    if request.method == 'POST':

        '''
        #First Method to delete
        for i in NewsLetter.objects.filter(status=1):

            check = request.POST.get(str(i.pk))

            if str(check) == 'on':
                ch = NewsLetter.objects.get(pk=i.pk)
                ch.delete()
'''     
        #Second method to delete
        check = request.POST.getlist('checks[]')
        
        for i in check:
            check = NewsLetter.objects.get(pk=i)
            check.delete()
        

    return redirect('news_email')



