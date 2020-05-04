from django.shortcuts import render, get_list_or_404, redirect, HttpResponse
from .models import UserManager
from django.contrib.auth import authenticate, login, logout
#Import  Users, Group, Permissions
from django.contrib.auth.models import User, Group, Permission
#To add permission to logged user to get which options use / this library very Important
from django.contrib.contenttypes.models import ContentType
#For regex password complexity verification
import re


def user_manager_list(request):

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

    manager = UserManager.objects.all().exclude(username="admin")

    return render(request, 'back/user_manager_list.html', {'manager':manager})

def user_delete(request, pk):

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

    #Deleting a user
    manager = UserManager.objects.get(pk=pk)

    #Deleing user in Django admin
    m = User.objects.filter(username=manager.username)
    m.delete()
    
    #Deleting user from User Manager App User List
    manager.delete()

    return redirect('user_manager_list')


def manage_group(request):

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
           

    #Retreiving groups(.exclude(name="masteruser"))
    group = Group.objects.all()

    return render(request, 'back/manage_group.html', {'group':group})

def manage_group_add(request):

     #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error': error})

    if request.method == 'POST':

        groupname = request.POST.get('groupname')

        if groupname != "":

            #Checking Whether Group Name Already Exists
            if len(Group.objects.filter(name=groupname)) == 0:

                #Saving Added Group Name
                group = Group(name=groupname)
                group.save()

    return redirect('manage_group')

def manage_group_del(request, word):

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
           
    group = Group.objects.filter(name=word)

    group.delete()

    return redirect('manage_group')

def users_group(request, pk):

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

    #Retreiving User details by pk method from models.py
    manager = UserManager.objects.get(pk=pk)

    #Saving User details from Django Admin to "user" variable
    user = User.objects.get(username=manager.username)

    ugroup = []
    #Retreiving  groups related to this particular User name
    for i in user.groups.all():
        ugroup.append(i.name)
    
    #Retreiving All group names from Django Admin
    group = Group.objects.all()
    
    return render(request, 'back/users_group.html', {'ugroup':ugroup, 'group':group, 'pk':pk, 'user':user})

#Here "pk" is UserManager model "pk" that is "username" "pk"
def add_user_togroup(request, pk):

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

        gname = request.POST.get('gname')

        #Retreiving group by "gname" from Django admin Group      
        group = Group.objects.get(name=gname)

        #Retreiving User details by pk method from models.py
        manager = UserManager.objects.get(pk=pk)

        #Retreiving User details from Django Admin to "user" variable
        user = User.objects.get(username=manager.username)

        #Adding current user to retrieved or selected group
        user.groups.add(group)

    return redirect('users_group', pk=pk)

def group_delete(request, pk, name):

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

    #Retreiving group by "word" from Django admin Group 
    group = Group.objects.get(name=name)

    #Retreiving User details by pk method from models.py
    manager = UserManager.objects.get(pk=pk)
    #Retreiving User details from Django Admin to "user" variable
    user = User.objects.get(username=manager.username)
    #This will remove group from that user
    user.groups.remove(group)

    #calling def users_group(request, pk):
    return redirect('users_group', pk=pk)

def manage_permission(request):

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
           

    #Retreiving Permissions
    permission = Permission.objects.all()

    return render(request, 'back/manage_permission.html', {'permission':permission})

def manage_permission_del(request, word):

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
           

    #Retreiving Permissions
    permission = Permission.objects.filter(name=word)
    permission.delete()

    return redirect('manage_permission')


def add_permission(request):

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

        permname = request.POST.get('permname')
        codname = request.POST.get('codname') 
        #checks whether permission with same name already exists
        if len(Permission.objects.filter(codename=codname)) == 0:
            #Addig Permission algorithm(Very Important)
            content_type = ContentType.objects.get(app_label='main', model='main')
            permisssion = Permission.objects.create(codename=codname, name=permname, content_type=content_type)
        
        else:
            error = "Name Already Exists!!!"
            return render(request, 'back/error.html',{'error': error})
        
    return redirect('manage_permission')


def users_perm(request, pk):

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

    #Retreiving User details by pk method from models.py
    manager = UserManager.objects.get(pk=pk)

    #Saving User details from Django Admin to "user" variable
    user = User.objects.get(username=manager.username)

    #Retreiving all Permissions
    permission = Permission.objects.all()

    upermission = Permission.objects.filter(user=user)
    uperm = []
    #Retreiving  permission related to this particular User name
    for i in upermission:
        uperm.append(i.name)
    
    
    return render(request, 'back/users_perm.html', {'uperm':uperm, 'permission': permission, 'pk':pk, 'user':user})


def users_permission_del(request, pk, word):

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

    #Retreiving User details by pk method from models.py
    manager = UserManager.objects.get(pk=pk)

    #Saving User details from Django Admin to "user" variable
    user = User.objects.get(username=manager.username)
           
    #Retreiving Permissions
    permission = Permission.objects.get(name=word)
    #Removing permission from specific user
    user.user_permissions.remove(permission)

    return redirect('users_perm', pk=pk)


def add_user_perm(request, pk):

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

        permname = request.POST.get('permname')

        #Retreiving group by "gname" from Django admin Group      
        permission= Permission.objects.get(name=permname)

        #Retreiving User details by pk method from models.py
        manager = UserManager.objects.get(pk=pk)

        #Retreiving User details from Django Admin to "user" variable
        user = User.objects.get(username=manager.username)

        #Adding Permission to current user
        user.user_permissions.add(permission)
        
    return redirect('users_perm', pk=pk)

def group_perm(request, pk):

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
 
     #Retreiving all permissions 
    permission = Permission.objects.all()
    #Saving group details by group pk
    group = Group.objects.get(pk=pk)
    #Saving specific permission by group to gperm
    gperm = group.permissions.all()
        
    return render(request, 'back/group_perm.html', {'gperm':gperm, 'pk':pk, 'permission':permission, 'group':group})


def group_permission_del(request, pk, name):

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


     #Saving Group details from Django Admin by group pk
    group = Group.objects.get(pk=pk)

     #Saving Permission details from Django Admin by permission name
    gperm = Permission.objects.get(name=name)

     #Removing permission from specific group
    group.permissions.remove(gperm)

    return redirect('group_perm', pk=pk)

def add_group_perm(request, pk):

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

        permname = request.POST.get('permname')

        #Saving permission by permission name    
        permission= Permission.objects.get(name=permname)

        #Saving Group details from Django Admin by group pk
        group = Group.objects.get(pk=pk)

        #Adding Permission to current group
        group.permissions.add(permission)
        
    return redirect('group_perm', pk=pk)
    
    