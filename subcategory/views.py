from django.shortcuts import render, get_list_or_404, redirect
from .models import SubCategory
from main.models import Main
from category.models import Category


def subcat_list(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    

    subcat = SubCategory.objects.all()
    return render(request, 'back/subcat_list.html', {'subcat': subcat})


def subcat_add(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    

    cat = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        catid = request.POST.get('cat')
        
        
        if name == "":
            error = "All Fields Required"
            return render(request, 'back/error.html',{'error': error})
        
        
        if len(SubCategory.objects.filter(name=name)) != 0:
            error = "Category Name already used"
            return render(request, 'back/error.html',{'error': error})

        catname = Category.objects.get(pk=catid).name
        subForm = SubCategory(name=name, catname=catname, catid=catid)
        subForm.save()
        return redirect('subcat_list')
    
    return render(request, 'back/subcat_add.html', {'cat': cat})