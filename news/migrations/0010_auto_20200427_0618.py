# Generated by Django 3.0.5 on 2020-04-27 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_news_activate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='activate',
            field=models.IntegerField(default=0),
        ),
    ]