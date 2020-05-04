from blacklist.models import BlackList

#Adding blacklisted IP every 5 minutes
def my_job():

    bl = BlackList(ip='162.165.25.255')
    bl.save()

     