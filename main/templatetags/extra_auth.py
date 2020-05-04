#1)Create a new folder under "main" folder name "templatetags"
#2)Create two files under "templatetags" 1)"__init__.py" and 2)"extra_auth.py"
#For setting permissions for users(User fom certain groups can access oly certain tempaltes(eg:news_add))

from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')

def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()