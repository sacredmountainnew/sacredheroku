from django.shortcuts import render, get_list_or_404, redirect
from .models import Category
from main.models import Main
#For exporting category list as CSV File
import csv
from django.http import HttpResponse


def cat_list(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    

    cat = Category.objects.all()
    return render(request, 'back/cat_list.html', {'cat': cat})


def cat_add(request):

    #login check started
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    

    
    if request.method == 'POST':
        name = request.POST.get('catname')
        
        if name == "":
            error = "All Fields Required"
            return render(request, 'back/error.html',{'error': error})
        
        
        if len(Category.objects.filter(name=name)) != 0:
            error = "Category Name already used"
            return render(request, 'back/error.html',{'error': error})

        
        catModel = Category(name=name)
        catModel.save()
        return redirect('cat_list')

    return render(request, 'back/cat_add.html')

#Exporting category list as CSV File
def cat_export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cat.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title','Counter'])

    for i in Category.objects.all():
        writer.writerow([i.name, i.count])
    
    return response

def import_cat_csv(request):

    if request.method == "POST":
        csv_file = request.FILES['csv_file']
        #Checking whether Csv file or not
        if not csv_file.name.endswith('.csv'):
            error = "File not supported"
            return render(request, 'back/error.html',{'error': error})
        #Checking whether file size is too large
        if csv_file.multiple_chunks():
            error = "Too large file"
            return render(request, 'back/error.html',{'error': error})


        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")

        for line in lines:
            fields = line.split(",")

            try:
                #Checking whether already with same category name exists
                if len(Category.objects.filter(name=fields[0])) == 0 and fields != "Title" and fields[0] != "":
                    cat = Category(name=fields[0])
                    cat.save()

            except:
                error = "Already this category name exists"
                return render(request, 'back/error.html',{'error': error})

    return redirect('cat_list')


