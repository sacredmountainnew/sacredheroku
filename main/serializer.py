from rest_framework import serializers
from news.models import News

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        #This is a filed in News Model(This will display in rest framework page)
        fields = ['name']