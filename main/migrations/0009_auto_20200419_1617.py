# Generated by Django 3.0.5 on 2020-04-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200408_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='picname',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='main',
            name='picurl',
            field=models.TextField(default=''),
        ),
    ]
