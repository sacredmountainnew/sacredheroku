# Generated by Django 3.0.5 on 2020-04-19 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200419_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='main',
            name='picnamefooter',
        ),
        migrations.RemoveField(
            model_name='main',
            name='picnameheader',
        ),
        migrations.RemoveField(
            model_name='main',
            name='picurlfooter',
        ),
        migrations.RemoveField(
            model_name='main',
            name='picurlheader',
        ),
    ]
