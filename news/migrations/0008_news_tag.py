# Generated by Django 3.0.5 on 2020-04-19 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_news_catid'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.TextField(default=''),
        ),
    ]